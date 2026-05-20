const API_URL = 'https://testing-automation-project.onrender.com/api';
let currentFilename = '';
let generatedTestCases = [];

document.getElementById('useAI').addEventListener('change', function() {
    document.getElementById('apiKeySection').style.display = this.checked ? 'block' : 'none';
});

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentFilename = data.filename;
            document.getElementById('uploadStatus').innerHTML = 
                `<p class="success">✓ File uploaded: ${data.filename}</p>`;
            document.getElementById('generateBtn').disabled = false;
        } else {
            document.getElementById('uploadStatus').innerHTML = 
                `<p class="error">✗ Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('uploadStatus').innerHTML = 
            `<p class="error">✗ Upload failed: ${error.message}</p>`;
    }
}

async function generateTests() {
    if (!currentFilename) {
        alert('Please upload a file first');
        return;
    }
    
    const useAI = document.getElementById('useAI').checked;
    const apiKey = document.getElementById('apiKey').value;
    
    if (useAI && !apiKey) {
        alert('Please enter OpenAI API key');
        return;
    }
    
    document.getElementById('testCasesDisplay').innerHTML = '<p class="info">Generating test cases...</p>';
    
    try {
        const response = await fetch(`${API_URL}/generate-tests`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                filename: currentFilename,
                use_ai: useAI,
                api_key: apiKey
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            generatedTestCases = data.test_cases;
            displayTestCases(data.test_cases);
            document.getElementById('executeBtn').disabled = false;
        } else {
            document.getElementById('testCasesDisplay').innerHTML = 
                `<p class="error">✗ Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('testCasesDisplay').innerHTML = 
            `<p class="error">✗ Generation failed: ${error.message}</p>`;
    }
}

function displayTestCases(testCases) {
    let html = `<p class="success">✓ Generated ${testCases.length} test cases</p><div class="test-results">`;
    
    testCases.forEach((test, index) => {
        html += `
            <div class="test-case">
                <h4>${index + 1}. ${test.name}</h4>
                <p><strong>Type:</strong> ${test.type}</p>
                <p><strong>Description:</strong> ${test.description}</p>
                <p><strong>Expected:</strong> ${test.expected}</p>
            </div>
        `;
    });
    
    html += '</div>';
    document.getElementById('testCasesDisplay').innerHTML = html;
}

async function executeTests() {
    if (generatedTestCases.length === 0) {
        alert('Please generate test cases first');
        return;
    }
    
    document.getElementById('executionResults').innerHTML = '<p class="info">Executing tests...</p>';
    
    try {
        const response = await fetch(`${API_URL}/execute-tests`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                test_cases: generatedTestCases,
                filename: currentFilename
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayExecutionResults(data.execution_result);
        } else {
            document.getElementById('executionResults').innerHTML = 
                `<p class="error">✗ Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('executionResults').innerHTML = 
            `<p class="error">✗ Execution failed: ${error.message}</p>`;
    }
}

function displayExecutionResults(result) {
    const passRate = ((result.passed / result.total) * 100).toFixed(1);
    
    let html = `
        <div class="stats">
            <div class="stat-box">
                <h3>${result.total}</h3>
                <p>Total Tests</p>
            </div>
            <div class="stat-box success">
                <h3>${result.passed}</h3>
                <p>Passed</p>
            </div>
            <div class="stat-box error">
                <h3>${result.failed}</h3>
                <p>Failed</p>
            </div>
            <div class="stat-box">
                <h3>${passRate}%</h3>
                <p>Pass Rate</p>
            </div>
        </div>
        <h3>Detailed Results</h3>
        <div class="test-results">
    `;
    
    result.results.forEach((test, index) => {
        const statusClass = test.status === 'passed' ? 'success' : 'error';
        html += `
            <div class="test-case ${statusClass}">
                <h4>${index + 1}. ${test.name}</h4>
                <p><strong>Type:</strong> ${test.type}</p>
                <p><strong>Description:</strong> ${test.description}</p>
                <p><strong>Status:</strong> <span class="${statusClass}">${test.status.toUpperCase()}</span></p>
                <p><strong>Message:</strong> ${test.message}</p>
            </div>
        `;
    });
    
    html += '</div>';
    document.getElementById('executionResults').innerHTML = html;
}
async function loadTestRuns() {
    try {
        const response = await fetch("https://testing-automation-project.onrender.com/api/get-test-runs");
        const data = await response.json();

        let html = "";

        if (data.runs.length === 0) {
            html = "<p>No test runs found</p>";
        } else {
            data.runs.forEach(run => {
                html += `
                    <div class="test-case">
                        <h4>${run.filename}</h4>
                        <p>Total: ${run.total_tests}</p>
                        <p>Passed: ${run.passed}</p>
                        <p>Failed: ${run.failed}</p>
                    </div>
                `;
            });
        }

        document.getElementById("testRunsContainer").innerHTML = html;

    } catch (error) {
        alert("Error loading test runs: " + error.message);
    }
}
