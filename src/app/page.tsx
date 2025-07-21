'use client'

import React, { useState } from 'react'
import axios, { AxiosError } from 'axios'
import BudgetForm from '../components/BudgetForm'

export default function Home() {
    const [submittedBudget, setSubmittedBudget] = useState<number | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const [successMessage, setSuccessMessage] = useState('')
    // set the error message to be displayed if the API call fails
    const [errorMessage, setErrorMessage] = useState('')
    const [apiResponse, setApiResponse] = useState<any>(null)

    const handleBudgetSubmit = async (budget: number) => {
        setIsLoading(true)
        
        try {
            // Call the FastAPI backend endpoint using axios
            const response = await axios.get(`http://localhost:8000/team-builder`, {
                params: {
                    budget: budget
                },
                timeout: 10000 // If the server is slow or unresponsive, the request will fail after the specified time (10 seconds here), allowing you to handle the error gracefully and keep your UI responsive.
            })
            
            const data = response.data

            // handle unsuccessful responses
                
            setSubmittedBudget(budget)
            setApiResponse(data)
            setSuccessMessage(`API Response: ${data.message}`)
            setErrorMessage('')
            
            console.log('API Response:', data)
            
        
        } catch (error: unknown) {
            console.error('Error submitting budget:', error)
            const axiosError = error as AxiosError<any>
            console.log('Axios Error:', axiosError)
            if (axiosError.response && axiosError.response.data) {
                const error_data = axiosError.response.data
                const error_detail = error_data.detail || error_data.message || 'An unexpected error occurred'
                setErrorMessage(`Error: ${error_detail}`)
                setSuccessMessage('')
                setApiResponse(null)
            }

        } finally {
            setIsLoading(false)
        }
    }

    const handleReset = () => {
        setSubmittedBudget(null)
        setSuccessMessage('')
        setErrorMessage('')
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

                    {/* if API errors, show an error message */}
                    {errorMessage && (
                        <div className="error-message">
                            {errorMessage}
                        </div>
                    )}
                
                    {submittedBudget !== null && apiResponse && (
                        <div className="budget-summary">
                            <h3 className="budget-summary-title">
                                Current Budget
                            </h3>
                            <p className="budget-summary-amount">
                                ${submittedBudget.toLocaleString()}
                            </p>
                            
                            

                            {/* if API response is successful display a table of products, showing name, category, price, and rating */}

                            {apiResponse && apiResponse.products && (
                                <div className="api-response-container">
                                    <h4 className='api-response-header'>API Response:</h4>
                                    <table className="product-table">
                                        <thead>
                                            <tr>
                                                <th>Name</th>
                                                <th>Category</th>
                                                <th>Price</th>
                                                <th>Rating</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {apiResponse.products.map((product: any) => (
                                                <tr key={product.id}>
                                                    <td>{product.name}</td>
                                                    <td>{product.category}</td>
                                                    <td>${product.price.toFixed(2)}</td>
                                                    <td>{product.rating ? product.rating.toFixed(2) : 'N/A'}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}

                            {/* if API response is an error, inform the user of the error */}
                            
                            <button
                                onClick={handleReset}
                                className="reset-button"
                            >
                            Reset Budget
                            </button>
                        </div>
                    )}
            </div>
        </div>
    )
}
