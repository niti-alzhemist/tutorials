/** @odoo-module **/

import {Component, useState} from "@odoo/owl"

export class Counter extends Component {
    static template = "awesome_owl.Counter"
    static props = {
        onChangeCallback: {
            type: Function,
            optional: true,

        }
    }

    setup() {
        this.state = useState({value: 1});
    }

    increment() {
        this.state.value++;
        if (this.props.onChangeCallback) {
            this.props.onChangeCallback();
        }
    }
}