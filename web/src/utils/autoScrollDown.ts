/**
 * Auto Scroll Down - Vanilla JS
 */
export function useAutoScrollDown() {
  let hadScrolledToBottom = true;
  const hasScrolledToBottom = (target: Element): boolean => {
    return (
      target.clientHeight + target.clientTop + target.scrollTop >
      target.scrollHeight
    );
  };
  const onScrollTarget = ({ target }: Event): void => {
    if (target instanceof Element) {
      hadScrolledToBottom = hasScrolledToBottom(target);
    }
  };
  const scrollToBottomIfNeeded = (target: Element): void => {
    if (hadScrolledToBottom) {
      target.scrollTo(0, target.scrollHeight);
    }
  };
  let childrenResizeObr: ResizeObserver | undefined;
  const targetMutationObr = new MutationObserver((entries) => {
    const entry = entries[0];
    for (const node of entry.removedNodes) {
      if (node instanceof Element) {
        childrenResizeObr?.unobserve(node);
      }
    }
    for (const node of entry.addedNodes) {
      if (node instanceof Element) {
        childrenResizeObr?.observe(node);
      }
    }
  });
  const mounted = (target: Element): void => {
    childrenResizeObr = new ResizeObserver(() =>
      scrollToBottomIfNeeded(target),
    );
    for (const child of target.children) {
      childrenResizeObr.observe(child);
    }
    targetMutationObr.observe(target, {
      childList: true,
    });
    target.addEventListener('scroll', onScrollTarget);
  };
  const unmounted = (target: Element): void => {
    childrenResizeObr?.disconnect();
    targetMutationObr.disconnect();
    target.removeEventListener('scroll', onScrollTarget);

    childrenResizeObr = undefined;
  };
  return { mounted, unmounted };
}

/**
 * Auto Scroll Down - Vue 3 Custom Directive
 * @example
 * ```vue
 * <template>
 *   <div v-auto-scroll-down>
 *     <div v-for="(item, index) in items" :key="index">
 *   </div>
 * </template>
 * <script setup>
 *   import { vAutoScrollDown } from '...';
 * </script>
 * ```
 */
export const vAutoScrollDown = useAutoScrollDown();
