import test from "node:test";
import assert from "node:assert/strict";
import { setImmediate } from "node:timers/promises";
import {
  createDeviceSessionStore,
  SessionOwnershipError,
} from "../src/device-session.mjs";
import {
  createAuthenticationService,
  createSignInAndRequestRefresh,
} from "../src/authentication.mjs";
import {
  createLoginConsumer,
  createReauthConsumer,
} from "../src/consumers.mjs";

const oldSession = { accountId: "same-user", accessToken: "old-token" };
const newSession = { accountId: "same-user", accessToken: "new-token" };
const localData = { accountId: "same-user", trips: ["기존 여행"] };

function deferred() {
  let resolve;
  let reject;
  const promise = new Promise((done, fail) => {
    resolve = done;
    reject = fail;
  });
  return { promise, resolve, reject };
}

function setup(overrides = {}) {
  const events = [];
  const refreshErrors = [];
  let persistedSession = structuredClone(oldSession);
  const deviceSession = createDeviceSessionStore({
    initialSession: oldSession,
    localData,
    async persistSession(session) {
      events.push("persist:start");
      await overrides.persistSession?.(session);
      persistedSession = session;
      events.push("persist:done");
    },
  });
  const authenticationService = createAuthenticationService({
    async requestAuthentication() {
      events.push("authenticate");
      return overrides.requestAuthentication
        ? overrides.requestAuthentication()
        : newSession;
    },
    async waitForActiveWork() {
      events.push("active-work:wait");
      await overrides.waitForActiveWork?.();
      events.push("active-work:done");
    },
    deviceSession,
  });
  const signInAndRequestRefresh = createSignInAndRequestRefresh({
    authenticationService,
    requestSessionRefresh() {
      // Query를 시작할 때 공개 상태와 저장된 세션이 일치하는지 확인한다.
      assert.deepEqual(deviceSession.readSnapshot().session, newSession);
      assert.deepEqual(persistedSession, newSession);
      events.push("refresh:request");
      return overrides.requestSessionRefresh?.();
    },
    onRefreshError(error) {
      refreshErrors.push(error);
      events.push("refresh:error");
    },
  });

  return {
    events,
    refreshErrors,
    deviceSession,
    signInAndRequestRefresh,
    readPersistedSession: () => structuredClone(persistedSession),
    onSignedIn(session) {
      assert.deepEqual(session, newSession);
      events.push("signed-in");
    },
  };
}

test("진행 작업과 기기 저장이 끝난 뒤 상태를 적용하고 Query 요청·인증 완료를 전달한다", async () => {
  const activeWork = deferred();
  const persistence = deferred();
  const query = deferred();
  const run = setup({
    waitForActiveWork: () => activeWork.promise,
    persistSession: () => persistence.promise,
    requestSessionRefresh: () => query.promise,
  });

  const result = run.signInAndRequestRefresh({}, { onSignedIn: run.onSignedIn });
  await setImmediate();
  assert.deepEqual(run.events, ["authenticate", "active-work:wait"]);
  assert.deepEqual(run.deviceSession.readSnapshot().session, oldSession);

  activeWork.resolve();
  await setImmediate();
  assert.equal(run.events.at(-1), "persist:start");
  assert.deepEqual(run.deviceSession.readSnapshot().session, oldSession);
  assert.deepEqual(run.readPersistedSession(), oldSession);

  persistence.resolve();
  assert.deepEqual(await result, newSession);
  assert.deepEqual(run.events, [
    "authenticate",
    "active-work:wait",
    "active-work:done",
    "persist:start",
    "persist:done",
    "refresh:request",
    "signed-in",
  ]);
  assert.deepEqual(run.deviceSession.readSnapshot().localData, localData);
  // Query를 끝내기 전에도 로그인 호출이 이미 완료됐다.
  query.resolve();
});

test("기기 저장 실패는 이전 상태·데이터를 보존하고 Query와 완료 알림을 시작하지 않는다", async () => {
  const failure = new Error("기기 저장 실패");
  const run = setup({ persistSession: async () => { throw failure; } });

  await assert.rejects(
    run.signInAndRequestRefresh({}, { onSignedIn: run.onSignedIn }),
    (error) => error === failure,
  );

  assert.deepEqual(run.deviceSession.readSnapshot(), {
    status: "signed-in",
    session: oldSession,
    localData,
  });
  assert.deepEqual(run.readPersistedSession(), oldSession);
  assert.equal(run.events.includes("refresh:request"), false);
  assert.equal(run.events.includes("signed-in"), false);
  assert.deepEqual(run.refreshErrors, []);
});

test("후속 Query 실패는 인증 성공을 되돌리거나 인증 호출 실패로 바꾸지 않는다", async () => {
  const query = deferred();
  const failure = new Error("조회 실패");
  const run = setup({ requestSessionRefresh: () => query.promise });

  assert.deepEqual(
    await run.signInAndRequestRefresh({}, { onSignedIn: run.onSignedIn }),
    newSession,
  );
  query.reject(failure);
  await setImmediate();

  assert.deepEqual(run.refreshErrors, [failure]);
  assert.deepEqual(run.deviceSession.readSnapshot().session, newSession);
  assert.deepEqual(run.readPersistedSession(), newSession);
  assert.deepEqual(run.deviceSession.readSnapshot().localData, localData);
  assert.deepEqual(run.events.slice(-3), [
    "refresh:request",
    "signed-in",
    "refresh:error",
  ]);
});

test("Query 요청 함수의 동기 오류도 후속 조회 실패로 처리한다", async () => {
  const failure = new Error("요청 시작 실패");
  const run = setup({ requestSessionRefresh() { throw failure; } });
  assert.deepEqual(
    await run.signInAndRequestRefresh({}, { onSignedIn: run.onSignedIn }),
    newSession,
  );
  assert.deepEqual(run.refreshErrors, [failure]);
  assert.equal(run.events.at(-1), "signed-in");
});

test("서버 인증 실패는 기기 저장·조회·완료 알림으로 진행하지 않는다", async () => {
  const failure = new Error("서버 인증 실패");
  const run = setup({ requestAuthentication: async () => { throw failure; } });
  await assert.rejects(
    run.signInAndRequestRefresh({}, { onSignedIn: run.onSignedIn }),
    (error) => error === failure,
  );
  assert.deepEqual(run.events, ["authenticate"]);
  assert.deepEqual(run.deviceSession.readSnapshot().session, oldSession);
});

test("다른 계정과 귀속 불명 데이터는 삭제하거나 덮어쓰지 않는다", async () => {
  for (const accountId of ["another-user", null]) {
    const data = { accountId, trips: ["보존할 여행"] };
    let writes = 0;
    const store = createDeviceSessionStore({
      localData: data,
      persistSession: async () => { writes += 1; },
    });
    await assert.rejects(store.applyAuthentication(newSession), SessionOwnershipError);
    assert.equal(writes, 0);
    assert.deepEqual(store.readSnapshot(), {
      status: "signed-out",
      session: null,
      localData: data,
    });
  }
});

test("Login과 Reauth 소비자는 인증 완료를 안내하고 각자 이동·닫기를 요청한다", async () => {
  const cases = [
    { create: createLoginConsumer, action: "navigateToTrips", message: "로그인 완료" },
    { create: createReauthConsumer, action: "closeDialog", message: "인증을 복구했어요" },
  ];

  for (const consumer of cases) {
    const query = deferred();
    const run = setup({ requestSessionRefresh: () => query.promise });
    const messages = [];
    let actionCalls = 0;
    const submit = consumer.create({
      signInAndRequestRefresh: run.signInAndRequestRefresh,
      showMessage: (message) => messages.push(message),
      [consumer.action]: () => { actionCalls += 1; },
    });

    await submit({});
    assert.deepEqual(messages, [consumer.message]);
    assert.equal(actionCalls, 1);
    assert.deepEqual(run.deviceSession.readSnapshot().session, newSession);
    query.resolve();
  }
});
