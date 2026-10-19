import { setImmediate } from "node:timers/promises";
import { createDeviceSessionStore } from "./device-session.mjs";
import {
  createAuthenticationService,
  createSignInAndRequestRefresh,
} from "./authentication.mjs";
import { createLoginConsumer } from "./consumers.mjs";

let persistedSession = null;
let finishRefresh;
let failRefresh;
const refresh = new Promise((resolve, reject) => {
  finishRefresh = resolve;
  failRefresh = reject;
});

const deviceSession = createDeviceSessionStore({
  localData: { accountId: "demo-user", trips: ["기존 여행"] },
  async persistSession(session) {
    persistedSession = session;
    console.log("1. 기기 저장 완료(메모리 어댑터)");
  },
});

const authenticationService = createAuthenticationService({
  async requestAuthentication() {
    return { accountId: "demo-user", accessToken: "demo-token" };
  },
  async waitForActiveWork() {
    // 실제 제품의 sync·cleanup·DB 작업 대신 즉시 종료하는 예시 어댑터다.
  },
  deviceSession,
});

const signInAndRequestRefresh = createSignInAndRequestRefresh({
  authenticationService,
  requestSessionRefresh() {
    console.log(`2. 공개 상태 확인: ${deviceSession.readSnapshot().status}`);
    console.log("3. Query 갱신 요청(아직 진행 중)");
    return refresh;
  },
  onRefreshError(error) {
    console.log(`6. 조회 후속 실패 별도 처리: ${error.message}`);
  },
});

const submitLogin = createLoginConsumer({
  signInAndRequestRefresh,
  showMessage(message) {
    console.log(`4. 완료 안내: ${message}`);
  },
  navigateToTrips() {
    console.log("5. Login 소비자의 이동 요청(UI 없음)");
  },
});

await submitLogin({ email: "demo@example.test" });

if (process.argv.includes("--refresh-fails")) {
  failRefresh(new Error("예시 조회 오류"));
} else {
  finishRefresh();
  console.log("6. 인증 완료 전달 이후 Query 갱신 완료");
}

await setImmediate();
const snapshot = deviceSession.readSnapshot();
console.log(
  `최종 상태: ${snapshot.status}, 저장 계정: ${persistedSession.accountId}, 보존한 여행: ${snapshot.localData.trips.length}개`,
);
