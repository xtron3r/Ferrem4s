async function getBookCover(query) {
    const apiKey = "AIzaSyBjOB_q4G9z4nsaQyjKOGX0vjGPtNt188s"; 
    const url = `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(query)}&key=${apiKey}`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        if (data.items && data.items.length > 0) {
            const bookInfo = data.items[0].volumeInfo;
            if (bookInfo.imageLinks && bookInfo.imageLinks.thumbnail) {
                return bookInfo.imageLinks.thumbnail;
            }
        }
        return 'No cover available';
    } catch (error) {
        console.error('Error fetching book cover:', error);
        return 'Error fetching cover';
    }
}

document.getElementById('search-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const query = document.getElementById('barra-busqueda').value;
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = 'Buscando...';
    const coverUrl = await getBookCover(query);
    resultDiv.innerHTML = `<img src="${coverUrl}" alt="Book Cover">`;
});

