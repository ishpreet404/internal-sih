import axios from "axios";

const API_BASE_URL =
	import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const api = axios.create({
	baseURL: API_BASE_URL,
	timeout: 300000, // 5 minutes for processing
});

export const apiService = {
	// Health check
	healthCheck: async () => {
		const response = await api.get("/health");
		return response.data;
	},

	// Upload files
	uploadFiles: async (files, options = {}) => {
		const formData = new FormData();

		files.forEach((file) => {
			formData.append("files", file);
		});

		if (options.ocrLanguage) {
			formData.append("ocrLanguage", options.ocrLanguage);
		}

		if (options.classificationMode) {
			formData.append("classificationMode", options.classificationMode);
		}

		const response = await api.post("/upload", formData, {
			headers: {
				"Content-Type": "multipart/form-data",
			},
		});

		return response.data;
	},

	// Process documents
	processDocuments: async (uploadedFiles, options = {}) => {
		const response = await api.post("/process", {
			files: uploadedFiles,
			ocr_language: options.ocrLanguage || "mal+eng",
			classification_mode: options.classificationMode || "railway",
		});

		return response.data;
	},

	// Chat with documents
	chatWithDocuments: async (message, processedData = null) => {
		const response = await api.post("/chat", {
			message,
			processed_data: processedData,
		});

		return response.data;
	},

	// Download data
	downloadData: async (dataType, data) => {
		const response = await api.post(`/download/${dataType}`, data);
		return response.data;
	},
};

export default apiService;
