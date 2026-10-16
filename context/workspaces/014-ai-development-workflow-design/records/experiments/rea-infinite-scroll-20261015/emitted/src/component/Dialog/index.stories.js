import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import Dialog from "../Dialog";
import Button from "../Button";
import { useAlertDialogStore } from "../../store/useAlertDialogStore";
import { useConfirmDialogStore } from "../../store/useConfirmDialogStore";
const meta = {
    title: "Common/Dialog",
    component: Dialog,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
export default meta;
export const Primary = {
    args: {
        children: _jsx("div", {}),
    },
    render: () => {
        return (_jsxs(Dialog, { children: [_jsx(Dialog.Trigger, { children: _jsx(Button, { children: "Open Dialog" }) }), _jsxs(Dialog.Content, { children: [_jsx(Dialog.Title, { children: "Dialog Title" }), _jsx(Dialog.Description, { children: "This is a description of the dialog content." }), _jsx(Dialog.Footer, { children: _jsx(Dialog.Cancel, { children: "Ok" }) })] })] }));
    },
};
export const WithFooter = {
    args: {
        children: _jsx("div", {}),
    },
    render: () => {
        const handleConfirm = () => {
            console.log("Confirm");
        };
        return (_jsxs(Dialog, { children: [_jsx(Dialog.Trigger, { children: _jsx(Button, { children: "Open Dialog" }) }), _jsxs(Dialog.Content, { children: [_jsx(Dialog.Title, { children: "Dialog Title" }), _jsx(Dialog.Description, { children: "This is a description of the dialog content." }), _jsxs(Dialog.Footer, { children: [_jsx(Dialog.Cancel, { children: "Cancel" }), _jsx(Dialog.Confirm, { callback: handleConfirm, children: "Confirm" })] })] })] }));
    },
};
export const ControlledAlertDialog = {
    args: {
        children: _jsx("div", {}),
    },
    render: () => {
        const { open, setOpen, title, description, setAlert, clearAlert } = useAlertDialogStore();
        return (_jsxs(_Fragment, { children: [_jsx(Button, { onClick: () => setAlert("Error", "This is a Network Error"), children: "Set Alert" }), _jsx(Dialog, { open: open, onOpenChange: setOpen, children: _jsxs(Dialog.Content, { children: [_jsx(Dialog.Title, { children: title }), _jsx(Dialog.Description, { children: description }), _jsx(Dialog.Footer, { children: _jsx(Dialog.Confirm, { callback: clearAlert, children: "Ok" }) })] }) })] }));
    },
};
export const ControlledConfirmDialog = {
    args: {
        children: _jsx("div", {}),
    },
    render: () => {
        const { open, setOpen, title, description, confirmCallback, clearConfirm, setConfirm, } = useConfirmDialogStore();
        return (_jsxs(_Fragment, { children: [_jsx(Button, { onClick: () => setConfirm("Confirm", "Are you sure?", () => {
                        console.log("Confirmed");
                    }), children: "Set Confirm" }), _jsx(Dialog, { open: open, onOpenChange: setOpen, children: _jsxs(Dialog.Content, { children: [_jsx(Dialog.Title, { children: title }), _jsx(Dialog.Description, { children: description }), _jsxs(Dialog.Footer, { children: [_jsx(Dialog.Cancel, { callback: clearConfirm, children: "Cancel" }), _jsx(Dialog.Confirm, { callback: confirmCallback, children: "Confirm" })] })] }) })] }));
    },
};
//# sourceMappingURL=index.stories.js.map