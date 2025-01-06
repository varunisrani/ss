const API_BASE_URL = 'http://127.0.0.1:5001/api';

export const generateReport = async (reportType, inputs) => {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

        const response = await fetch(`${API_BASE_URL}/generate-report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                report_type: reportType,
                inputs: {
                    ...inputs,
                    timestamp: new Date().toISOString()
                }
            }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timeout - please try again');
        }
        if (error.message === 'Failed to fetch') {
            throw new Error('Unable to connect to server - please check if the server is running');
        }
        console.error('API Error:', error);
        throw error;
    }
};

export const fetchReports = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/reports`);
        if (!response.ok) {
            throw new Error('Failed to fetch reports');
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}; 