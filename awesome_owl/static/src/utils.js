/** @odoo-module */

import {useEffect, useRef} from "@odoo/owl";

export const useAutoFocus = (name) => {
    const ref = useRef(name)
    useEffect(
        () => ref.el && ref.el.focus(),
        () => [ref.el]
    );
}