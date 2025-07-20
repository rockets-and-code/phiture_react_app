'use client'

import React, { useState } from 'react'

interface BudgetFormProps {
    onSubmit: (budget: number) => void
    isLoading?: boolean
}

const BudgetForm: React.FC<BudgetFormProps> = ({ onSubmit, isLoading = false }) => {
    const [budget, setBudget] = useState<string>('')
    const [error, setError] = useState<string>('')

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        setError('')

        // Validate input
        if (!budget.trim()) {
            setError('Please enter a budget amount')
            return
        }

        const budgetNumber = parseFloat(budget)
        
        if (isNaN(budgetNumber)) {
            setError('Please enter a valid number')
            return
        }

        if (budgetNumber < 0) {
            setError('Budget must be a positive number')
            return
        }

        // Call the onSubmit callback with the budget value
        onSubmit(budgetNumber)
        
        // Reset form on successful submission
        setBudget('')
    }

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
        setBudget(value)
        
        // Clear error when user starts typing
        if (error) {
            setError('')
        }
    }

    return (
        <form onSubmit={handleSubmit}>
        <div className="form-group">
            <label htmlFor="budget" className="label">
            Budget Amount
            </label>
            <input
            type="number"
            id="budget"
            value={budget}
            onChange={handleInputChange}
            placeholder="Enter your budget (e.g., 1000.00)"
            className="input"
            step="0.01"
            min="0"
            disabled={isLoading}
            />
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <button
            type="submit"
            className="button"
            disabled={isLoading}
        >
            {isLoading ? 'Submitting...' : 'Submit Budget'}
        </button>
        </form>
    )
}

export default BudgetForm
