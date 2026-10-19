export class SessionOwnershipError extends Error {
  constructor() {
    super("기존 계정 또는 로컬 데이터의 귀속을 확인해야 합니다.");
    this.name = "SessionOwnershipError";
  }
}

export function createDeviceSessionStore({
  initialSession = null,
  localData = { accountId: null, trips: [] },
  persistSession,
}) {
  let session = structuredClone(initialSession);
  const retainedData = structuredClone(localData);

  return {
    readSnapshot() {
      return structuredClone({
        status: session ? "signed-in" : "signed-out",
        session,
        localData: retainedData,
      });
    },

    async applyAuthentication(nextSession) {
      const candidate = structuredClone(nextSession);
      const belongsToAnotherAccount =
        session && session.accountId !== candidate.accountId;
      const hasUnmatchedData =
        retainedData.trips.length > 0 &&
        retainedData.accountId !== candidate.accountId;

      if (belongsToAnotherAccount || hasUnmatchedData) {
        throw new SessionOwnershipError();
      }

      // 저장이 실패하면 공개 상태와 보존한 여행 데이터를 바꾸지 않는다.
      await persistSession(structuredClone(candidate));
      session = candidate;
      return structuredClone(session);
    },
  };
}
