document.addEventListener("DOMContentLoaded", function() {
  fetch("http://localhost:5000/api/gifts") // Ambil data dari backend Flask
    .then(response => response.json())
    .then(data => {
      let gallery = document.getElementById("gallery");
      gallery.innerHTML = ""; // Kosongkan sebelum menambah data baru
      data.forEach(item => {
        let div = document.createElement("div");
        div.className = "gift-item";
        div.innerHTML = `
          <a href="${item.link}" target="_blank">
            <img src="${item.link}" alt="NFT Gift">
          </a>
          <p><b>${item.name}</b> - ${item.price}</p>
        `;
        gallery.appendChild(div);
      });
    })
    .catch(error => console.error("Gagal mengambil data:", error));
});