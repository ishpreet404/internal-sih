import React from 'react'
import { FileText, Tag, Eye, Brain, Download, Clock, Globe, FileCheck } from 'lucide-react'
import { motion } from 'framer-motion'
import clsx from 'clsx'

const ResultsTab = ({ data, files }) => {
  const handleDownload = (type) => {
    let content = ''
    let filename = ''

    switch (type) {
      case 'ocr':
        content = data?.ocr_text || ''
        filename = 'ocr_results.txt'
        break
      case 'summary':
        content = data?.summary || ''
        filename = 'ai_summary.txt'
        break
      default:
        return
    }

    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.9) return 'bg-green-100 text-green-800'
    if (confidence >= 0.7) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const getConfidenceLabel = (confidence) => {
    if (confidence >= 0.9) return 'High'
    if (confidence >= 0.7) return 'Medium'
    return 'Low'
  }

  if (!data) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Processing Results</h2>
          <p className="text-lg text-gray-600">
            View OCR results, AI summaries, and document classifications
          </p>
        </div>

        <div className="bg-white border border-gray-200 rounded-xl p-12 text-center">
          <FileCheck className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Results Yet</h3>
          <p className="text-gray-600">
            Upload and process documents to see results here.
          </p>
        </div>
      </div>
    )
  }

  // Handle potential API errors
  if (data.error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Processing Results</h2>
          <p className="text-lg text-gray-600">
            View OCR results, AI summaries, and document classifications
          </p>
        </div>

        <div className="bg-red-50 border border-red-200 rounded-xl p-12 text-center">
          <div className="text-red-500 mb-4">⚠️</div>
          <h3 className="text-xl font-semibold text-red-900 mb-2">Processing Error</h3>
          <p className="text-red-700">
            {data.error}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Processing Results</h2>
        <p className="text-lg text-gray-600">
          View OCR results, AI summaries, and document classifications
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Document Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="flex items-center space-x-2 text-lg font-semibold text-gray-900">
              <FileText className="h-5 w-5 text-primary-600" />
              <span>Document Overview</span>
            </h3>
          </div>
          <div className="card-content space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-600">Document Type</label>
              <p className="text-lg font-semibold text-gray-900">{data.document_type}</p>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-600">Total Pages</label>
                <p className="text-lg font-semibold text-gray-900">{data.metadata?.total_pages || files.length}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Files Processed</label>
                <p className="text-lg font-semibold text-gray-900">{data.metadata?.files_processed || files.length}</p>
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-600">Languages Detected</label>
              <div className="flex flex-wrap gap-2 mt-1">
                {data.metadata?.languages_detected?.map((lang, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                  >
                    <Globe className="h-3 w-3 mr-1" />
                    {lang}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-600">Processing Details</label>
              <div className="text-sm text-gray-700 space-y-1">
                <p>OCR Language: {data.metadata?.ocr_language}</p>
                <p>Classification Mode: {data.metadata?.classification_mode}</p>
                <p>Characters Extracted: {data.metadata?.total_characters?.toLocaleString()}</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Railway Classification */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="flex items-center space-x-2 text-lg font-semibold text-gray-900">
              <Tag className="h-5 w-5 text-primary-600" />
              <span>Railway Classification</span>
            </h3>
          </div>
          <div className="card-content space-y-3">
            {data.classification && data.classification.length > 0 ? (
              data.classification.map((item, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <span className="font-medium text-gray-900">{item.category}</span>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-600">
                      {Math.round(item.confidence * 100)}%
                    </span>
                    <span className={clsx(
                      'px-2 py-1 rounded-full text-xs font-medium',
                      getConfidenceColor(item.confidence)
                    )}>
                      {getConfidenceLabel(item.confidence)}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 italic text-center py-4">
                No railway classifications available
              </p>
            )}
          </div>
        </motion.div>
      </div>

      {/* OCR Results */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card mb-8"
      >
        <div className="card-header">
          <h3 className="flex items-center space-x-2 text-lg font-semibold text-gray-900">
            <Eye className="h-5 w-5 text-primary-600" />
            <span>OCR Extracted Text</span>
          </h3>
          <button
            onClick={() => handleDownload('ocr')}
            className="btn btn-secondary btn-small"
          >
            <Download className="h-4 w-4" />
            Download
          </button>
        </div>
        <div className="card-content">
          <div className="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
            <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono">
              {data.ocr_text || 'No OCR text available'}
            </pre>
          </div>
        </div>
      </motion.div>

      {/* AI Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="flex items-center space-x-2 text-lg font-semibold text-gray-900">
            <Brain className="h-5 w-5 text-primary-600" />
            <span>AI Summary</span>
          </h3>
          <button
            onClick={() => handleDownload('summary')}
            className="btn btn-secondary btn-small"
          >
            <Download className="h-4 w-4" />
            Download
          </button>
        </div>
        <div className="card-content">
          <div className="prose max-w-none">
            <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
              {data.summary || 'No AI summary available'}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Key Information (if available) */}
      {data.key_information && Object.keys(data.key_information).length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="card mt-8"
        >
          <div className="card-header">
            <h3 className="flex items-center space-x-2 text-lg font-semibold text-gray-900">
              <FileCheck className="h-5 w-5 text-primary-600" />
              <span>Key Information</span>
            </h3>
          </div>
          <div className="card-content">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(data.key_information).map(([category, items]) => (
                items && items.length > 0 && (
                  <div key={category}>
                    <h4 className="font-medium text-gray-900 mb-2">
                      {category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </h4>
                    <ul className="space-y-1">
                      {items.slice(0, 5).map((item, index) => (
                        <li key={index} className="text-sm text-gray-600">
                          • {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                )
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default ResultsTab