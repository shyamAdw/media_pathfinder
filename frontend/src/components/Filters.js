import React from 'react';

const Filters = ({ customerId, onCustomerIdChange, campaignStatus, onCampaignStatusChange, onFetchData }) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Customer ID"
        value={customerId}
        onChange={(e) => onCustomerIdChange(e.target.value)}
      />
      <select value={campaignStatus} onChange={(e) => onCampaignStatusChange(e.target.value)}>
        <option value="ENABLED">Enabled</option>
        <option value="PAUSED">Paused</option>
        {/* Add other status options if needed */}
      </select>
      <button onClick={onFetchData}>Fetch Data</button>
    </div>
  );
};

export default Filters;