import React, { useState, useEffect } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

const AccessMatrix = ({ users, resources }) => {
    const [decisions, setDecisions] = useState({});
    const [riskScores, setRiskScores] = useState({});
    
    // Generate column definitions
    const [columnDefs, setColumnDefs] = useState([
        { headerName: 'User/Resource', field: 'user', pinned: 'left' }
    ]);
    setRiskScores({user1: 0.5, user2: 0.8,
    });
    useEffect(() => {
        // Dynamic columns based on resources
        const resourceColumns = resources.map(resource => ({
            headerName: resource.name,
            field: `resource_${resource.id}`,
            cellRenderer: params => {
                const decision = decisions[`${params.data.userId}_${resource.id}`];
                const riskScore = riskScores[`${params.data.userId}_${resource.id}`];
                if (!decision) return null;
                
                return (
                    <div className={`decision-cell ${decision.allowed ? 'allowed' : 'denied'}`}>
                        {decision.allowed ? '✓' : '✗'}
                        <div className="risk-badge" style={{ 
                            backgroundColor: getRiskColor(riskScore)
                        }}>
                            {riskScore}
                        </div>
                    </div>
                );
            },
            tooltipValueGetter: params => {
                const decision = decisions[`${params.data.userId}_${resource.id}`];
                return decision ? decision.reason : '';
            }
        }));
        
        setColumnDefs([{ headerName: 'User/Resource', field: 'user', pinned: 'left' }, ...resourceColumns]);
    }, [resources, decisions, riskScores]);

    
    const getRiskColor = score => {
        if (score < 0.3) return '#2ecc71';
        if (score < 0.7) return '#f39c12';
        return '#e74c3c';
    };
    
    const onGridReady = params => {
        params.api.sizeColumnsToFit();

        // Simulate fetching access decisions
        const mockDecisions = {};
        users.forEach(user => {
            resources.forEach(resource => {
                const key = `${user.id}_${resource.id}`;
                const allowed = Math.random() > 0.5;
                const riskScore = Math.round(Math.random() * 100) / 100;
                mockDecisions[key] = {
                    allowed,
                    riskScore,
                    reason: allowed 
                        ? `Access granted based on ${user.roles.join(', ')} roles` 
                        : `Access denied - insufficient privileges`
                };
            });
        });
        
        setDecisions(mockDecisions);
        
        // Generate row data
        const rowData = users.map(user => ({
            user: user.name,
            userId: user.id,
            ...resources.reduce((acc, resource) => {
                acc[`resource_${resource.id}`] = `${user.id}_${resource.id}`;
                return acc;
            }, {})
        }));
        
        params.api.setRowData(rowData);
    };
    
    return (
    <div>
        <div className="ag-theme-alpine" style={{ height: '600px', width: '100%' }}>
            <AgGridReact
                columnDefs={columnDefs}
                rowData={[]}
                onGridReady={onGridReady}
                suppressCellFocus={true}
                tooltipShowDelay={100}
            />
        </div>
    </div>
    );
};

export default AccessMatrix;