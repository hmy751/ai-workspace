import { isOfflineError } from '@/shared/services/offline-prep/errors';

/** Router의 제한 이유는 보존하고 일반 요청 실패에는 기존 화면 문구를 사용한다. */
export function mutationErrorMessage(error: unknown, fallback: string): string {
  return isOfflineError(error) ? error.message : fallback;
}
