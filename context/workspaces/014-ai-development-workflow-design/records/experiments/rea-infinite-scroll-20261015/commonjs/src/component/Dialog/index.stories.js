"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ControlledConfirmDialog = exports.ControlledAlertDialog = exports.WithFooter = exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const Dialog_1 = __importDefault(require("../Dialog"));
const Button_1 = __importDefault(require("../Button"));
const useAlertDialogStore_1 = require("../../store/useAlertDialogStore");
const useConfirmDialogStore_1 = require("../../store/useConfirmDialogStore");
const meta = {
    title: "Common/Dialog",
    component: Dialog_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
exports.default = meta;
exports.Primary = {
    args: {
        children: (0, jsx_runtime_1.jsx)("div", {}),
    },
    render: () => {
        return ((0, jsx_runtime_1.jsxs)(Dialog_1.default, { children: [(0, jsx_runtime_1.jsx)(Dialog_1.default.Trigger, { children: (0, jsx_runtime_1.jsx)(Button_1.default, { children: "Open Dialog" }) }), (0, jsx_runtime_1.jsxs)(Dialog_1.default.Content, { children: [(0, jsx_runtime_1.jsx)(Dialog_1.default.Title, { children: "Dialog Title" }), (0, jsx_runtime_1.jsx)(Dialog_1.default.Description, { children: "This is a description of the dialog content." }), (0, jsx_runtime_1.jsx)(Dialog_1.default.Footer, { children: (0, jsx_runtime_1.jsx)(Dialog_1.default.Cancel, { children: "Ok" }) })] })] }));
    },
};
exports.WithFooter = {
    args: {
        children: (0, jsx_runtime_1.jsx)("div", {}),
    },
    render: () => {
        const handleConfirm = () => {
            console.log("Confirm");
        };
        return ((0, jsx_runtime_1.jsxs)(Dialog_1.default, { children: [(0, jsx_runtime_1.jsx)(Dialog_1.default.Trigger, { children: (0, jsx_runtime_1.jsx)(Button_1.default, { children: "Open Dialog" }) }), (0, jsx_runtime_1.jsxs)(Dialog_1.default.Content, { children: [(0, jsx_runtime_1.jsx)(Dialog_1.default.Title, { children: "Dialog Title" }), (0, jsx_runtime_1.jsx)(Dialog_1.default.Description, { children: "This is a description of the dialog content." }), (0, jsx_runtime_1.jsxs)(Dialog_1.default.Footer, { children: [(0, jsx_runtime_1.jsx)(Dialog_1.default.Cancel, { children: "Cancel" }), (0, jsx_runtime_1.jsx)(Dialog_1.default.Confirm, { callback: handleConfirm, children: "Confirm" })] })] })] }));
    },
};
exports.ControlledAlertDialog = {
    args: {
        children: (0, jsx_runtime_1.jsx)("div", {}),
    },
    render: () => {
        const { open, setOpen, title, description, setAlert, clearAlert } = (0, useAlertDialogStore_1.useAlertDialogStore)();
        return ((0, jsx_runtime_1.jsxs)(jsx_runtime_1.Fragment, { children: [(0, jsx_runtime_1.jsx)(Button_1.default, { onClick: () => setAlert("Error", "This is a Network Error"), children: "Set Alert" }), (0, jsx_runtime_1.jsx)(Dialog_1.default, { open: open, onOpenChange: setOpen, children: (0, jsx_runtime_1.jsxs)(Dialog_1.default.Content, { children: [(0, jsx_runtime_1.jsx)(Dialog_1.default.Title, { children: title }), (0, jsx_runtime_1.jsx)(Dialog_1.default.Description, { children: description }), (0, jsx_runtime_1.jsx)(Dialog_1.default.Footer, { children: (0, jsx_runtime_1.jsx)(Dialog_1.default.Confirm, { callback: clearAlert, children: "Ok" }) })] }) })] }));
    },
};
exports.ControlledConfirmDialog = {
    args: {
        children: (0, jsx_runtime_1.jsx)("div", {}),
    },
    render: () => {
        const { open, setOpen, title, description, confirmCallback, clearConfirm, setConfirm, } = (0, useConfirmDialogStore_1.useConfirmDialogStore)();
        return ((0, jsx_runtime_1.jsxs)(jsx_runtime_1.Fragment, { children: [(0, jsx_runtime_1.jsx)(Button_1.default, { onClick: () => setConfirm("Confirm", "Are you sure?", () => {
                        console.log("Confirmed");
                    }), children: "Set Confirm" }), (0, jsx_runtime_1.jsx)(Dialog_1.default, { open: open, onOpenChange: setOpen, children: (0, jsx_runtime_1.jsxs)(Dialog_1.default.Content, { children: [(0, jsx_runtime_1.jsx)(Dialog_1.default.Title, { children: title }), (0, jsx_runtime_1.jsx)(Dialog_1.default.Description, { children: description }), (0, jsx_runtime_1.jsxs)(Dialog_1.default.Footer, { children: [(0, jsx_runtime_1.jsx)(Dialog_1.default.Cancel, { callback: clearConfirm, children: "Cancel" }), (0, jsx_runtime_1.jsx)(Dialog_1.default.Confirm, { callback: confirmCallback, children: "Confirm" })] })] }) })] }));
    },
};
//# sourceMappingURL=index.stories.js.map