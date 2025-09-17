import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, Image, X, Settings, Play } from 'lucide-react'
import { motion } from 'framer-motion'
import clsx from 'clsx'

const UploadTab = ({ files, onFileUpload, onFileRemove, onProcess, isProcessing }) => {
  const [ocrLanguage, setOcrLanguage] = useState('mal+eng')
  const [classificationMode, setClassificationMode] = useState('railway')

  const onDrop = useCallback((acceptedFiles) => {
    onFileUpload(acceptedFiles)
  }, [onFileUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    multiple: true
  })

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (file) => {
    if (file.type === 'application/pdf') {
      return <FileText className="h-6 w-6 text-red-500" />
    }
    return <Image className="h-6 w-6 text-blue-500" />
  }

  const handleProcess = () => {
    onProcess({
      ocrLanguage,
      classificationMode
    })
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Upload Documents</h2>
        <p className="text-lg text-gray-600">
          Upload railway documents for OCR processing, AI analysis, and classification
        </p>
      </div>

      {/* Upload Area */}
      <motion.div
        {...getRootProps()}
        className={clsx(
          'border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300',
          isDragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        )}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <input {...getInputProps()} />
        <Upload className="h-16 w-16 text-primary-500 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          {isDragActive ? 'Drop files here' : 'Drag & Drop Files Here'}
        </h3>
        <p className="text-gray-600 mb-2">
          or <span className="text-primary-600 font-medium">browse files</span>
        </p>
        <p className="text-sm text-gray-500">
          Supports: PDF, PNG, JPG, JPEG
        </p>
      </motion.div>

      {/* File List */}
      {files.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Uploaded Files ({files.length})
          </h3>
          <div className="space-y-3">
            {files.map((file, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg shadow-sm"
              >
                <div className="flex items-center space-x-3">
                  {getFileIcon(file)}
                  <div>
                    <h4 className="font-medium text-gray-900">{file.name}</h4>
                    <p className="text-sm text-gray-500">{formatFileSize(file.size)}</p>
                  </div>
                </div>
                <button
                  onClick={() => onFileRemove(index)}
                  className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-all duration-200"
                >
                  <X className="h-4 w-4" />
                </button>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Processing Options */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Settings className="h-4 w-4" />
            <span>OCR Language</span>
          </label>
          <select
            value={ocrLanguage}
            onChange={(e) => setOcrLanguage(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200"
          >
            <option value="mal+eng">Malayalam + English</option>
            <option value="eng">English</option>
            <option value="mal">Malayalam</option>
            <option value="hin+eng">Hindi + English</option>
          </select>
        </div>

        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Settings className="h-4 w-4" />
            <span>Classification Mode</span>
          </label>
          <select
            value={classificationMode}
            onChange={(e) => setClassificationMode(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200"
          >
            <option value="railway">Railway Documents</option>
            <option value="general">General Documents</option>
            <option value="both">Both</option>
          </select>
        </div>
      </motion.div>

      {/* Process Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mt-8 text-center"
      >
        <motion.button
          onClick={handleProcess}
          disabled={files.length === 0 || isProcessing}
          className={clsx(
            'inline-flex items-center space-x-2 px-8 py-3 rounded-lg font-semibold text-lg transition-all duration-200',
            files.length === 0 || isProcessing
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-primary-600 text-white hover:bg-primary-700 shadow-lg hover:shadow-xl'
          )}
          whileHover={files.length > 0 && !isProcessing ? { scale: 1.05 } : {}}
          whileTap={files.length > 0 && !isProcessing ? { scale: 0.95 } : {}}
        >
          <Play className="h-5 w-5" />
          <span>Process Documents</span>
        </motion.button>
      </motion.div>
    </div>
  )
}

export default UploadTab