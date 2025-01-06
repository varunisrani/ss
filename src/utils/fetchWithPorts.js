export async function fetchWithPorts(endpoint, options = {}) {
    const port = 5002; // Only using port 5002
    let response;
    try {
        response = await fetch(`http://127.0.0.1:${port}${endpoint}`, options);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.error(`Error fetching from port ${port}:`, error);
    }
    throw new Error('Failed to fetch from port 5002');
} 