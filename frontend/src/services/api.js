const API_BASE_URL = '/api'; // Using proxy in development

export const fetchData = async (customerId, campaignStatus) => {
  const response = await fetch(`${API_BASE_URL}/data?customerId=${customerId}&campaignStatus=${campaignStatus}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const drillDown = async (customerId, campaignStatus, nodeId) => {
    const response = await fetch(`${API_BASE_URL}/drilldown?customerId=${customerId}&campaignStatus=${campaignStatus}&nodeId=${nodeId}`);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

export const authenticateWithGoogle = async (code) => {
  const response = await fetch(`${API_BASE_URL}/authenticate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code }),
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.json();
};