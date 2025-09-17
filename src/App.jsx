import React, { useState } from 'react'
import { motion } from 'framer-motion'
import Header from './components/Header'
import UploadTab from './components/UploadTab'
import ChatTab from './components/ChatTab'
import ResultsTab from './components/ResultsTab'
import ProcessingModal from './components/ProcessingModal'
import Toast from './components/Toast'
import Footer from './components/Footer'
import { apiService } from './services/api'

function App() {
  const [activeTab, setActiveTab] = useState('upload')
  const [files, setFiles] = useState([])
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [processedData, setProcessedData] = useState(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [processingStatus, setProcessingStatus] = useState('')
  const [progress, setProgress] = useState(0)
  const [toasts, setToasts] = useState([])

  const addToast = (toast) => {
    const id = Date.now()
    const newToast = { ...toast, id }
    setToasts(prev => [...prev, newToast])
    
    // Auto remove after 5 seconds
    setTimeout(() => {
      removeToast(id)
    }, 5000)
  }

  const removeToast = (id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id))
  }

  const handleFileUpload = (newFiles) => {
    setFiles(prev => [...prev, ...newFiles])
    addToast({
      type: 'success',
      title: 'Files Added',
      message: `${newFiles.length} file(s) added successfully`
    })
  }

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index))
  }

  const processDocuments = async (options) => {
    if (files.length === 0) {
      addToast({
        type: 'error',
        title: 'No Files',
        message: 'Please upload files before processing'
      })
      return
    }

    setIsProcessing(true)
    setProgress(0)
    setProcessingStatus('Uploading files...')

    try {
      // Step 1: Upload files (20%)
      setProgress(20)
      const uploadResult = await apiService.uploadFiles(files, options)
      setUploadedFiles(uploadResult.files)

      // Step 2: Process documents (40-90%)
      setProcessingStatus('Processing documents...')
      setProgress(40)

      // Simulate progress updates during processing
      const progressUpdates = [
        { status: 'Running OCR...', progress: 50 },
        { status: 'Analyzing content...', progress: 65 },
        { status: 'Generating summary...', progress: 80 },
        { status: 'Classifying documents...', progress: 90 },
      ]

      for (const update of progressUpdates) {
        setProcessingStatus(update.status)
        setProgress(update.progress)
        await new Promise(resolve => setTimeout(resolve, 500))
      }

      // Final processing
      setProcessingStatus('Finalizing results...')
      setProgress(95)
      
      const result = await apiService.processDocuments(uploadResult.files, options)
      
      setProgress(100)
      setProcessedData(result)
      setActiveTab('results')
      
      addToast({
        type: 'success',
        title: 'Processing Complete',
        message: 'Documents processed successfully'
      })

    } catch (error) {
      console.error('Processing error:', error)
      addToast({
        type: 'error',
        title: 'Processing Failed',
        message: error.response?.data?.error || error.message || 'An error occurred during processing'
      })
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1 container mx-auto px-4 py-8">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'upload' && (
            <UploadTab
              files={files}
              onFileUpload={handleFileUpload}
              onFileRemove={removeFile}
              onProcess={processDocuments}
              isProcessing={isProcessing}
            />
          )}
          
          {activeTab === 'chat' && (
            <ChatTab
              processedData={processedData}
              isEnabled={!!processedData}
            />
          )}
          
          {activeTab === 'results' && (
            <ResultsTab
              data={processedData}
              files={files}
            />
          )}
        </motion.div>
      </main>

      <Footer />

      <ProcessingModal
        isOpen={isProcessing}
        status={processingStatus}
        progress={progress}
      />

      <div className="fixed top-4 right-4 z-50 space-y-2">
        {toasts.map(toast => (
          <Toast
            key={toast.id}
            {...toast}
            onClose={() => removeToast(toast.id)}
          />
        ))}
      </div>
    </div>
  )
}

export default App