"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const clsx_1 = __importDefault(require("clsx"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
// --- Component ---
const Grid = (0, react_1.forwardRef)(({ columns, gap = '24px', minChildWidth = '280px', children, className, style, ...restProps }, ref) => {
    const gridStyles = (0, react_1.useMemo)(() => {
        const newStyles = {
            ...style,
            '--grid-gap': `${gap}`,
        };
        if (columns) {
            switch (typeof columns) {
                case 'number':
                    newStyles['--grid-columns'] = columns.toString();
                    break;
                case 'object':
                    if (columns?.base) {
                        newStyles['--grid-columns-base'] = columns.base.toString();
                    }
                    if (columns.sm) {
                        newStyles['--grid-columns-sm'] = columns.sm.toString();
                    }
                    if (columns.md) {
                        newStyles['--grid-columns-md'] = columns.md.toString();
                    }
                    if (columns.lg) {
                        newStyles['--grid-columns-lg'] = columns.lg.toString();
                    }
                    if (columns.xl) {
                        newStyles['--grid-columns-xl'] = columns.xl.toString();
                    }
                    break;
            }
        }
        else {
            newStyles['--grid-min-child-width'] = typeof minChildWidth === 'number' ? `${minChildWidth}px` : minChildWidth;
        }
        return newStyles;
    }, [columns, gap, minChildWidth, style]);
    const gridClasses = (0, clsx_1.default)(index_module_css_1.default.grid, 
    // columns prop 존재 여부에 따라 다른 클래스를 부여하여 CSS에서 분기 처리
    columns ? index_module_css_1.default.explicitColumns : index_module_css_1.default.autoFillColumns, className);
    return ((0, jsx_runtime_1.jsx)("div", { ref: ref, className: gridClasses, style: gridStyles, ...restProps, children: children }));
});
exports.default = Grid;
//# sourceMappingURL=index.js.map