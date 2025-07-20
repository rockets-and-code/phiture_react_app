'use client'

import React, { useState } from 'react'
import axios from 'axios'
import BudgetForm from '../components/BudgetForm'

export default function Home() {
    const [submittedBudget, setSubmittedBudget] = useState<number | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const [successMessage, setSuccessMessage] = useState('')
    const [apiResponse, setApiResponse] = useState<any>(null)

  const handleBudgetSubmit = async (budget: number) => {
    setIsLoading(true)
    
    try {
      // Call the FastAPI backend endpoint using axios
      const response = await axios.get(`http://localhost:8000/team-builder`, {
        params: {
          budget: budget
        },
        timeout: 10000 // 10 second timeout
      })
      
      const data = response.data
      
      setSubmittedBudget(budget)
      setApiResponse(data)
      setSuccessMessage(`API Response: ${data.message}`)
      
      console.log('API Response:', data)
      
      // Clear success message after 8 seconds
      setTimeout(() => {
        setSuccessMessage('')
      }, 8000)
      
    } catch (error) {
      console.error('Error submitting budget:', error)
      
      let errorMessage = 'Error: Unable to connect to the backend API.'
      
      if (axios.isAxiosError(error)) {
        if (error.response) {
          // Server responded with error status
          errorMessage = `Error: Server responded with status ${error.response.status}`
        } else if (error.request) {
          // Request was made but no response received
          errorMessage = 'Error: No response from server. Please make sure the backend is running on port 8000.'
        } else {
          // Something else happened
          errorMessage = `Error: ${error.message}`
        }
      }
      
      setSuccessMessage(errorMessage)
      
      // Clear error message after 8 seconds
      setTimeout(() => {
        setSuccessMessage('')
      }, 8000)
    } finally {
      setIsLoading(false)
    }
  }

    const handleReset = () => {
        setSubmittedBudget(null)
        setSuccessMessage('')
        setApiResponse(null)
    }

    return (
        <div className="container">
            <div className="card">
                <h1 className="title">Budget Input</h1>
                <p className="subtitle">Enter your budget amount below</p>
                
                <BudgetForm 
                    onSubmit={handleBudgetSubmit}
                    isLoading={isLoading}
                />
                    {successMessage && (
                        <div className="success-message">
                            {successMessage}
                        </div>
                    )}
                
                    {submittedBudget !== null && (
                        <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
                            <h3 style={{ color: '#374151', marginBottom: '0.5rem' }}>
                                Current Budget
                            </h3>
                            <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#059669' }}>
                                ${submittedBudget.toLocaleString()}
                            </p>
                            
                            {apiResponse && (
                                <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#f3f4f6', borderRadius: '6px', textAlign: 'left' }}>
                                    <h4 style={{ color: '#374151', marginBottom: '0.5rem', textAlign: 'center' }}>API Response:</h4>
                                    <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                                        <p><strong>Status:</strong> {apiResponse.status}</p>
                                        <p><strong>Message:</strong> {apiResponse.message}</p>
                                        <p><strong>Budget:</strong> ${apiResponse.budget?.toLocaleString() || 'N/A'}</p>
                                    </div>
                                </div>
                            )}
                            
                            <button
                                onClick={handleReset}
                                style={{
                                    marginTop: '1rem',
                                    padding: '0.5rem 1rem',
                                    backgroundColor: '#6b7280',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '6px',
                                    cursor: 'pointer',
                                    fontSize: '0.875rem'
                                }}
                            >
                            Reset Budget
                            </button>
                        </div>
                    )}
            </div>
        </div>
    )
}
