'use client'

import { useState } from 'react'
import EditTodoModal from './EditTodoModal'
import { format, parseISO } from 'date-fns'
import { AlertTriangle, Calendar, Clock, CheckCircle, Flag } from 'lucide-react'

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

interface TodoCardProps {
  todo: Todo
  onUpdate: (id: string, updates: Partial<Todo>) => void
  onDelete: (id: string) => void
  onToggleComplete: (todo: Todo) => void
}

export default function TodoCard({ todo, onUpdate, onDelete, onToggleComplete }: TodoCardProps) {
  const [showEditModal, setShowEditModal] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleUpdate = async (title: string, description?: string, due_date?: string, priority?: 'low' | 'medium' | 'high') => {
    setLoading(true)
    try {
      await onUpdate(todo.id, { title, description, due_date, priority })
      setShowEditModal(false)
    } catch (error) {
      console.error('Error updating todo:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        await onDelete(todo.id)
      } catch (error) {
        console.error('Error deleting todo:', error)
      }
    }
  }

  const formatDate = (dateString?: string) => {
    if (!dateString) return null
    try {
      return format(parseISO(dateString), 'MMM dd, yyyy')
    } catch {
      return dateString
    }
  }

  // Determine the border color based on completion status, priority, and due date
  const getBorderColor = () => {
    if (todo.completed) return 'border-green-500'
    if (todo.due_date && new Date(todo.due_date) < new Date()) return 'border-red-500'
    if (todo.priority === 'high') return 'border-red-500'
    if (todo.priority === 'medium') return 'border-amber-500'
    return 'border-blue-500'
  }

  // Determine the priority badge color
  const getPriorityColor = () => {
    switch (todo.priority) {
      case 'high': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
      case 'medium': return 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300'
      case 'low': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  // Get priority icon
  const getPriorityIcon = () => {
    switch (todo.priority) {
      case 'high': return <AlertTriangle className="h-4 w-4" />
      case 'medium': return <Flag className="h-4 w-4" />
      case 'low': return <Flag className="h-4 w-4" />
      default: return <Flag className="h-4 w-4" />
    }
  }

  // Check if the todo is overdue
  const isOverdue = !todo.completed && todo.due_date && new Date(todo.due_date) < new Date()

  return (
    <div className={`bg-white dark:bg-gray-700/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border-l-4 transition-all duration-300 transform hover:scale-[1.02] hover:shadow-xl ${getBorderColor()} ${
      todo.completed ? 'opacity-80' : ''
    }`}>
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggleComplete(todo)}
          className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500 mt-0.5"
        />
        <div className="ml-4 flex-1">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className={`text-lg font-semibold ${
                todo.completed
                  ? 'text-gray-500 dark:text-gray-400 line-through'
                  : 'text-gray-900 dark:text-white'
              }`}>
                {todo.title}
              </h3>
              {todo.description && (
                <p className="mt-2 text-gray-600 dark:text-gray-300">
                  {todo.description}
                </p>
              )}
            </div>
            {todo.priority && (
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor()}`}>
                {getPriorityIcon()}
                <span className="ml-1 capitalize">{todo.priority}</span>
              </span>
            )}
          </div>

          <div className="mt-4 space-y-2">
            {todo.due_date && (
              <div className={`flex items-center text-sm ${isOverdue ? 'text-red-600 dark:text-red-400' : 'text-gray-500 dark:text-gray-400'}`}>
                <Calendar className="h-4 w-4 mr-1.5 flex-shrink-0" />
                <span>Due: {formatDate(todo.due_date)}</span>
                {isOverdue && (
                  <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300">
                    <Clock className="h-3 w-3 mr-1" />
                    Overdue
                  </span>
                )}
              </div>
            )}
            <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
              <CheckCircle className="h-3.5 w-3.5 mr-1.5 flex-shrink-0" />
              <span>Created: {formatDate(todo.created_at)}</span>
            </div>
          </div>

          <div className="mt-4 flex justify-between items-center">
            <div className="flex space-x-2">
              <button
                onClick={() => setShowEditModal(true)}
                className="text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300 p-1 rounded hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors"
                title="Edit todo"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button
                onClick={handleDelete}
                className="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 p-1 rounded hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                title="Delete todo"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
            {todo.completed && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">
                <CheckCircle className="h-3 w-3 mr-1" />
                Completed
              </span>
            )}
          </div>
        </div>
      </div>

      {showEditModal && (
        <EditTodoModal
          todo={todo}
          onClose={() => setShowEditModal(false)}
          onUpdate={handleUpdate}
          loading={loading}
        />
      )}
    </div>
  )
}