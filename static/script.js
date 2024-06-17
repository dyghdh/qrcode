function generateQRCode() {
    const eventId = document.getElementById('event-id').value;
    if (!eventId) {
        alert('이벤트 ID를 입력하세요');
        return;
    }

    fetch('/generate_qr', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ event_id: eventId })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const qrCode = document.getElementById('qr-code');
        qrCode.innerHTML = `<img src="${url}" alt="QR Code">`;

        const downloadLink = document.getElementById('download-link');
        downloadLink.href = url;
        downloadLink.download = 'qr_code.png';
        downloadLink.style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}

function fetchAttendance() {
    fetch('/attendance')
        .then(response => response.json())
        .then(data => {
            const attendanceList = document.getElementById('attendance-list');
            attendanceList.innerHTML = '';
            data.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = item;
                attendanceList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error:', error));
}
