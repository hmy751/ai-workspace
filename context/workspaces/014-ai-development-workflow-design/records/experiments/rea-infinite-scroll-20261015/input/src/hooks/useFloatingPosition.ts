import { useState, useEffect, CSSProperties } from 'react';

type FloatingStyles = CSSProperties;

/**
 * 트리거 요소를 기준으로 떠 있는(floating) 요소의 위치를 계산하는 커스텀 훅
 * @param triggerElement - 위치의 기준이 되는 트리거 요소
 * @param floatingElement - 위치를 계산할 떠 있는 요소
 * @param isOpen - 떠 있는 요소가 현재 보이는지 여부
 * @param gap - 트리거와 떠 있는 요소 사이의 간격 (기본값: 4px)
 * @returns {FloatingStyles} - 적용할 style 객체
 */
const useFloatingPosition = (
  triggerElement: HTMLElement | null,
  floatingElement: HTMLElement | null,
  isOpen: boolean,
  gap = 4
): FloatingStyles => {
  const [styles, setStyles] = useState<FloatingStyles>({
    position: 'absolute',
    top: -9999,
    left: -9999,
    minWidth: 0,
  });


  useEffect(() => {
    if (!isOpen || !triggerElement || !floatingElement) {
      return;
    }

    const calculatePosition = () => {
      if (!triggerElement || !floatingElement) return;

      const triggerRect = triggerElement.getBoundingClientRect();

      const floatingHeight = floatingElement.offsetHeight;
      const windowHeight = window.innerHeight;

      let top = triggerRect.bottom + window.scrollY + gap;

      // 메뉴가 화면 아래쪽 경계를 벗어나는지 확인하고 위로 뒤집기(flip)
      if (top + floatingHeight > windowHeight + window.scrollY) {
        top = triggerRect.top + window.scrollY - floatingHeight - gap;
      }

      setStyles({
        position: 'absolute',
        top,
        left: triggerRect.left + window.scrollX,
        minWidth: triggerRect.width,
      });
    };

    calculatePosition();

    window.addEventListener('resize', calculatePosition);
    window.addEventListener('scroll', calculatePosition, true);

    return () => {
      window.removeEventListener('resize', calculatePosition);
      window.removeEventListener('scroll', calculatePosition, true);
    };
  }, [isOpen, triggerElement, floatingElement, gap]);


  return styles;
};

export default useFloatingPosition;