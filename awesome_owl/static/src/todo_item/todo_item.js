/** @odoo-module **/

import {Component} from "@odoo/owl"
import {CheckBox} from "@web/core/checkbox/checkbox";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem"
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        onCheckCallback: Function,
        onRemoveCallback: Function
    }

    static components = {CheckBox}

    handleToggleCheckBox(ev) {
        this.props.onCheckCallback(ev.target.checked, this.props.todo.id)
    }

    handleToggleRemove() {
        this.props.onRemoveCallback(this.props.todo.id)
    }
}