import React, { useState, useEffect } from 'react';
import WaterfallChart from './components/WaterfallChart';
import Filters from './components/Filters';
import './App.css';
import { fetchData, authenticateWithGoogle } from './services/api';

function App() {
  const [data, setData] = useState(null);
  const [customerId, setCustomerId] = useState('YOUR_TEST_CUSTOMER_ID'); // Replace with actual customer ID input
  const [campaignStatus, setCampaignStatus] = useState('ENABLED'); // Example status
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    if (code) {
      authenticateWithGoogle(code)
        .then(response => {
          if (response.message === 'Authentication successful') {
            setIsAuthenticated(true);
            window.history.replaceState({}, document.title, "/");
          } else {
            console.error('Authentication failed');
          }
        })
        .catch(error => console.error('Authentication error:', error));
    }
  }, []);

  const handleDataFetch = () => {
    fetchData(customerId, campaignStatus)
      .then(apiData => setData(apiData))
      .catch(error => console.error("Error fetching data:", error));
  };

  const handleGoogleSignIn = () => {
    const clientId = 'YOUR_GOOGLE_CLIENT_ID'; // Replace with your actual Google Client ID
    const redirectUri = encodeURIComponent('http://localhost:3000');
    const scope = encodeURIComponent('https://www.googleapis.com/auth/adwords');
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=<span class="math-inline">\{clientId\}&redirect\_uri\=</span>{redirectUri}&response_type=code&scope=${scope}&access_type=offline&prompt=consent`;
    window.location.href = authUrl;
  };

  return (
    <div className="App">
      <h1>Media Pathfinder</h1>
      {!isAuthenticated ? (
        <button onClick={handleGoogleSignIn}>Sign in with Google</button>
      ) : (
        <>
          <Filters
            customerId={customerId}
            onCustomerIdChange={setCustomerId}
            campaignStatus={campaignStatus}
            onCampaignStatusChange={setCampaignStatus}
            onFetchData={handleDataFetch}
          />
          {data && <WaterfallChart data={data} customerId={customerId} campaignStatus={campaignStatus} />}
        </>
      )}
    </div>
  );
}

export default App;