async function convertPDFtoWord() {
    const pdfInput = document.getElementById('pdfInput');
    pdfInput.click(); // Trigger the file input's click event
  
    pdfInput.addEventListener('change', async () => {
      const file = pdfInput.files[0];
  
      if (!file || file.type !== 'application/pdf') {
        alert('Please select a valid PDF file.');
        return;
      }
  
      try {
        const formData = new FormData();
        formData.append('pdf_file', file);
  
        const response = await fetch('/convert', {
          method: 'POST',
          body: formData
        });
  
        const data = await response.json();
        const resultDiv = document.getElementById('result');
  
        if (data.success) {
          const downloadLink = document.createElement('a');
          downloadLink.href = data.url; // This should include the route for downloading the file
          downloadLink.download = 'converted.docx';
          downloadLink.textContent = 'Download Word file';
  
          resultDiv.innerHTML = '<p>Conversion successful! Click the link below to download the Word file.</p>';
          resultDiv.appendChild(downloadLink);
        } else {
          resultDiv.innerHTML = `<p>Conversion failed. ${data.message}</p>`;
        }
      } catch (error) {
        console.error('Error:', error);
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<p>An error occurred. Please try again later.</p>`;
      }
    });
  }
  