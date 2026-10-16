"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const clsx_1 = __importDefault(require("clsx"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
const Input = (0, react_1.forwardRef)(({ placeholder, isFocused: controlledFocus, onFocus, onChangeFocus, onBlur, isTouched: controlledTouch, onTouchStart, onMouseDown, onChangeTouch, isError, disabled, isDisabled, className, ...restProps }, ref) => {
    // ref 처리
    const internalInputRef = (0, react_1.useRef)(null);
    const assignRef = (0, react_1.useCallback)((element) => {
        if (element) {
            internalInputRef.current = element;
        }
        if (typeof ref === "function") {
            ref(element);
        }
        else if (ref) {
            ref.current = element;
        }
    }, [ref]);
    // isTouched와 같은 value는 control, unControl에 따라서 기준을 정하고,
    // 이벤트는 control, unControl 모두 실행하여 일관성을 유지한다.
    // touch 이벤트
    const [unControlledTouch, setUnControlledTouch] = (0, react_1.useState)(false);
    const isControlledTouch = controlledTouch !== undefined;
    const isTouched = isControlledTouch ? controlledTouch : unControlledTouch;
    const handleTouch = (e) => {
        e.stopPropagation();
        // 내부 unControlled 상태 이벤트
        setUnControlledTouch(true);
        // 단순 boolean 상태 이벤트
        onChangeTouch?.(true);
        // 상위 useForm과 같은 controlled 상태 이벤트
        onTouchStart?.(e);
        onMouseDown?.(e);
    };
    // focus 이벤트
    const [unControlledFocus, setUncontrolledFocus] = (0, react_1.useState)(false);
    const isControlledFocus = controlledFocus !== undefined;
    const isFocused = isControlledFocus ? controlledFocus : unControlledFocus;
    const handleFocus = (0, react_1.useCallback)((e) => {
        e.stopPropagation();
        setUncontrolledFocus(true);
        onChangeFocus?.(true);
        onFocus?.(e);
    }, [onChangeFocus, onFocus]);
    // blur 이벤트
    const handleBlur = (0, react_1.useCallback)((e) => {
        e.stopPropagation();
        setUncontrolledFocus(false);
        onChangeFocus?.(false);
        onBlur?.(e);
    }, [onChangeFocus, onBlur, isControlledFocus]);
    return ((0, jsx_runtime_1.jsx)("input", { ref: assignRef, placeholder: placeholder, disabled: disabled, className: (0, clsx_1.default)(index_module_css_1.default.input, isTouched && index_module_css_1.default.isTouched, isFocused && index_module_css_1.default.isFocused, isError && index_module_css_1.default.isError, isError
            ? "global-focus-visible-error"
            : "global-focus-visible-default", disabled && index_module_css_1.default.isDisabled, className), onMouseDown: handleTouch, onTouchStart: handleTouch, onFocus: handleFocus, onBlur: handleBlur, ...restProps }));
});
Input.displayName = "Input";
exports.default = Input;
//# sourceMappingURL=index.js.map