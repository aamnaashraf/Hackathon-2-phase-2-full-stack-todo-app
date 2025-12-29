'use client'

import { useState, useMemo } from 'react'
import TodoCard from './TodoCard'
import AddTodoModal from './AddTodoModal'
import { createTodo, updateTodo, deleteTodo } from '@/lib/api'
import { useToast } from '@/lib/toast'
import { Search, Filter, Calendar, Clock, CheckCircle2, AlertCircle, XCircle } from 'lucide-react'

interface Todo {
  id: string
  title: string
  description?: string
  completed: boolean
  user_id: string
  created_at: string
  updated_at: string
  due_date?: string
  priority?: 'low' | 'medium' | 'high'
}

interface TodoListProps {
  todos: Todo[]
  setTodos: React.Dispatch<React.SetStateAction<Todo[]>>
}

export default function TodoList({ todos, setTodos }: TodoListProps) {
  const [showAddModal, setShowAddModal] = useState(false)
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending' | 'overdue' | 'high-priority'>('all')
  const [sort, setSort] = useState<'due_date' | 'priority' | 'alphabetical' | 'created'>('due_date')
  const { showToast } = useToast()

  // Filter and sort todos
  const filteredAndSortedTodos = useMemo(() => {
    let result = [...todos]

    // Apply search filter
    if (searchTerm) {
      result = result.filter(todo =>
        todo.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (todo.description && todo.description.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    }

    // Apply status filter
    if (filter === 'completed') {
      result = result.filter(todo => todo.completed)
    } else if (filter === 'pending') {
      result = result.filter(todo => !todo.completed)
    } else if (filter === 'overdue') {
      result = result.filter(todo =>
        !todo.completed &&
        todo.due_date &&
        new Date(todo.due_date) < new Date()
      )
    } else if (filter === 'high-priority') {
      result = result.filter(todo =>
        !todo.completed &&
        todo.priority === 'high'
      )
    }

    // Apply sorting
    result.sort((a, b) => {
      if (sort === 'due_date') {
        if (!a.due_date && !b.due_date) return 0
        if (!a.due_date) return 1
        if (!b.due_date) return -1
        return new Date(a.due_date).getTime() - new Date(b.due_date).getTime()
      } else if (sort === 'priority') {
        const priorityOrder = { high: 3, medium: 2, low: 1 }
        const aPriority = priorityOrder[a.priority || 'low']
        const bPriority = priorityOrder[b.priority || 'low']
        if (aPriority !== bPriority) return bPriority - aPriority
        // If priorities are the same, sort by due date
        if (!a.due_date && !b.due_date) return 0
        if (!a.due_date) return 1
        if (!b.due_date) return -1
        return new Date(a.due_date).getTime() - new Date(b.due_date).getTime()
      } else if (sort === 'alphabetical') {
        return a.title.localeCompare(b.title)
      } else { // created
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      }
    })

    return result
  }, [todos, searchTerm, filter, sort])

  const handleAddTodo = async (title: string, description?: string, due_date?: string, priority?: 'low' | 'medium' | 'high') => {
    setLoading(true)
    try {
      const newTodo = await createTodo(title, description, due_date, priority)
      setTodos((prev) => [...prev, newTodo])
      setShowAddModal(false)
      showToast('Todo added successfully!', 'success')
    } catch (error: any) {
      console.error('Error adding todo:', error)
      const errorMessage = error.message || 'Failed to add todo. Please try again.'
      showToast(errorMessage, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateTodo = async (id: string, updates: Partial<Todo>) => {
    try {
      const updatedTodo = await updateTodo(id, updates)
      setTodos((prev) => prev.map(todo => todo.id === id ? updatedTodo : todo))
      showToast('Todo updated successfully!', 'success')
    } catch (error: any) {
      console.error('Error updating todo:', error)
      showToast(error.message || 'Failed to update todo. Please try again.', 'error')
    }
  }

  const handleDeleteTodo = async (id: string) => {
    try {
      await deleteTodo(id)
      setTodos((prev) => prev.filter(todo => todo.id !== id))
      showToast('Todo deleted successfully!', 'info')
    } catch (error: any) {
      console.error('Error deleting todo:', error)
      showToast(error.message || 'Failed to delete todo. Please try again.', 'error')
    }
  }

  const handleToggleComplete = async (todo: Todo) => {
    try {
      const updatedTodo = await updateTodo(todo.id, { completed: !todo.completed })
      setTodos((prev) => prev.map(t => t.id === todo.id ? updatedTodo : t))
      showToast(todo.completed ? 'Todo marked as incomplete' : 'Todo marked as complete!', 'success')
    } catch (error: any) {
      console.error('Error toggling todo completion:', error)
      showToast(error.message || 'Failed to update todo status. Please try again.', 'error')
    }
  }

  return (
    <div className="space-y-6">
      {/* Search and Filter Controls */}
      <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
        <div className="relative w-full md:w-64">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Search todos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:text-white"
          />
        </div>

        <div className="flex flex-wrap gap-3 w-full md:w-auto">
          <div className="flex items-center space-x-2">
            <Filter className="h-5 w-5 text-gray-500 dark:text-gray-400" />
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as any)}
              className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="all">All Todos</option>
              <option value="completed">Completed</option>
              <option value="pending">Pending</option>
              <option value="overdue">Overdue</option>
              <option value="high-priority">High Priority</option>
            </select>
          </div>

          <div className="flex items-center space-x-2">
            <Clock className="h-5 w-5 text-gray-500 dark:text-gray-400" />
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value as any)}
              className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="due_date">Sort by Due Date</option>
              <option value="priority">Sort by Priority</option>
              <option value="alphabetical">Sort Alphabetically</option>
              <option value="created">Sort by Created Date</option>
            </select>
          </div>
        </div>
      </div>

      {/* Add Todo Button */}
      <div className="flex justify-end">
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-6 py-3 rounded-lg flex items-center transition-all duration-200 transform hover:scale-105 shadow-lg"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Add Todo
        </button>
      </div>

      {/* Todo List or Empty State */}
      {filteredAndSortedTodos.length === 0 ? (
        <div className="text-center py-16">
          <div className="mx-auto w-24 h-24 bg-gradient-to-br from-indigo-100 to-purple-100 dark:from-indigo-900/30 dark:to-purple-900/30 rounded-full flex items-center justify-center mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">No todos found</h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            {searchTerm || filter !== 'all'
              ? 'Try adjusting your search or filter criteria'
              : 'Get started by creating a new todo.'
            }
          </p>
          {!searchTerm && filter === 'all' && (
            <button
              onClick={() => setShowAddModal(true)}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Create your first todo
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAndSortedTodos.map((todo) => (
            <TodoCard
              key={todo.id}
              todo={todo}
              onUpdate={handleUpdateTodo}
              onDelete={handleDeleteTodo}
              onToggleComplete={handleToggleComplete}
            />
          ))}
        </div>
      )}

      {showAddModal && (
        <AddTodoModal
          onClose={() => setShowAddModal(false)}
          onAdd={handleAddTodo}
          loading={loading}
        />
      )}
    </div>
  )
}
