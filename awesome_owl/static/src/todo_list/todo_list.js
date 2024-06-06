/** @odoo-module **/

import {Component, onMounted, useRef, useState} from "@odoo/owl"
import {TodoItem} from "../todo_item/todo_item";
import {useAutoFocus} from "../utils"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList"
    static components = {TodoItem}


    setup() {
        useAutoFocus('input')
        this.todos = useState({
            value: []
        });
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            const cloneTodo = [...this.todos.value]
            cloneTodo.sort((a, b) => a.id - b.id)
            const latestTodo = cloneTodo[cloneTodo.length - 1]
            const nextId = (latestTodo ? latestTodo.id : 0) + 1
            const newTodo = {
                id: nextId,
                description: ev.target.value,
                isCompleted: false,
            }
            this.todos.value = [...cloneTodo, newTodo,]
        }
    }

    handleOnCheckCallback(check, id) {
        const cloneTodo = [...this.todos.value]
        cloneTodo[cloneTodo.findIndex(item => item.id === id)].isCompleted = check
        this.todos.value = cloneTodo
    }

    handleOnRemoveCallback(id) {
        const cloneTodo = [...this.todos.value]
        const index = cloneTodo.findIndex(item => item.id === id)
        if (index >= 0) {
            cloneTodo.splice(index, 1)
        }
        this.todos.value = cloneTodo
    }
}