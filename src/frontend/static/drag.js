// 配置项
const CONFIG = {
    MOVE_THRESHOLD: 5,
    EXCLUDE_TAGS: new Set(['INPUT', 'TEXTAREA', 'SELECT']),
    TEXT_SELECT_CLASS: 'rcs-allow-select',
    DATA_ALLOW_SELECT: 'data-rcs-allow-select',
    SCROLL_CONTAINER_CLASS: 'rcs-scroll-zone',
    INERTIA_DECAY: 0.95,
    INERTIA_MIN_SPEED: 0.5
};

// 样式注入（如果使用的是原生 JS 环境而非 Greasemonkey）
function addStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .rcs-scroll-active {
            cursor: grab !important;
            user-select: none !important;
        }
        .rcs-scroll-active.grabbing {
            cursor: grabbing !important;
        }
        .${CONFIG.TEXT_SELECT_CLASS}, [${CONFIG.DATA_ALLOW_SELECT}] {
            user-select: text !important;
        }
    `;
    document.head.appendChild(style);
}

class InstantRightClickScroll {
    #container = null;
    #startPos = { x: 0, y: 0 };
    #scrollPos = { x: 0, y: 0 };
    #lastMoveTime = 0;
    #lastDelta = { x: 0, y: 0 };
    #isDragging = false;
    #hasMoved = false;

    constructor() {
        document.addEventListener('mousedown', e => this.#handleStart(e));
    }

    #shouldIgnore(target) {
        return (
            CONFIG.EXCLUDE_TAGS.has(target.tagName) ||
            target.isContentEditable ||
            !!target.closest(`.${CONFIG.TEXT_SELECT_CLASS}, [${CONFIG.DATA_ALLOW_SELECT}]`)
        );
    }

    #findScrollContainer(el) {
        const marked = el.closest(`.${CONFIG.SCROLL_CONTAINER_CLASS}`);
        if (marked) return marked;

        let current = el;
        while (current && current !== document.documentElement) {
            const style = getComputedStyle(current);
            const overflow = `${style.overflow}${style.overflowY}${style.overflowX}`;
            if (
                (current.scrollHeight > current.clientHeight || current.scrollWidth > current.clientWidth) &&
                /(auto|scroll)/.test(overflow)
            ) {
                return current;
            }
            current = current.parentElement;
        }

        return document.scrollingElement;
    }

    #handleStart(e) {
        if (e.button !== 2 || this.#shouldIgnore(e.target)) return;

        this.#container = this.#findScrollContainer(e.target);
        if (!this.#container) return;

        this.#startPos = { x: e.clientX, y: e.clientY };
        this.#scrollPos = {
            x: this.#container.scrollLeft,
            y: this.#container.scrollTop
        };
        this.#hasMoved = false;
        this.#isDragging = false;
        this.#lastMoveTime = Date.now();
        this.#lastDelta = { x: 0, y: 0 };

        const moveHandler = e => this.#handleMove(e);
        const upHandler = e => this.#handleEnd(e, cleanUp);
        const contextMenuHandler = e => {
            if (this.#hasMoved) {
                e.preventDefault();
                e.stopImmediatePropagation();
            }
        };

        const cleanUp = () => {
            document.removeEventListener('mousemove', moveHandler);
            document.removeEventListener('mouseup', upHandler);
            document.removeEventListener('contextmenu', contextMenuHandler);
            if (this.#isDragging) {
                this.#container.classList.remove('rcs-scroll-active');
            }
            this.#isDragging = false;
        };

        document.addEventListener('mousemove', moveHandler);
        document.addEventListener('mouseup', upHandler);
        document.addEventListener('contextmenu', contextMenuHandler, true);
    }

    #handleMove(e) {
        const dx = e.clientX - this.#startPos.x;
        const dy = e.clientY - this.#startPos.y;

        if (!this.#isDragging) {
            if (Math.abs(dx) + Math.abs(dy) < CONFIG.MOVE_THRESHOLD) return;
            this.#isDragging = true;
            this.#container.classList.add('rcs-scroll-active');
            e.preventDefault();
        }

        const newX = this.#scrollPos.x - dx;
        const newY = this.#scrollPos.y - dy;

        this.#lastDelta = {
            x: this.#container.scrollLeft - newX,
            y: this.#container.scrollTop - newY
        };

        this.#container.scrollLeft = newX;
        this.#container.scrollTop = newY;
        this.#hasMoved = true;
    }

    #handleEnd(e, cleanUp) {
        if (e.button === 2 && this.#hasMoved) {
            e.preventDefault();
            e.stopImmediatePropagation();

            const speed = { ...this.#lastDelta };
            const frame = () => {
                speed.x *= CONFIG.INERTIA_DECAY;
                speed.y *= CONFIG.INERTIA_DECAY;

                if (Math.abs(speed.x) < CONFIG.INERTIA_MIN_SPEED && Math.abs(speed.y) < CONFIG.INERTIA_MIN_SPEED) {
                    return;
                }

                this.#container.scrollLeft -= speed.x;
                this.#container.scrollTop -= speed.y;
                requestAnimationFrame(frame);
            };
            requestAnimationFrame(frame);

            const tempAllow = ev => {
                document.removeEventListener('contextmenu', tempAllow);
                document.removeEventListener('mousedown', tempAllow);
            };
            document.addEventListener('contextmenu', tempAllow, { once: true });
            document.addEventListener('mousedown', tempAllow, { once: true });
        }

        cleanUp();
    }
}

// 初始化
addStyles();
new InstantRightClickScroll();