async function loadNFTs() {
    try {
        let response = await fetch("http://206.189.44.231:5000/api/nfts");
        let nfts = await response.json();
        let gallery = document.getElementById("gallery");
        gallery.innerHTML = "";

        if (nfts.length === 0) {
            gallery.innerHTML = "<p>Belum ada NFT.</p>";
            return;
        }

        nfts.forEach(nft => {
            let div = document.createElement("div");
            div.className = "gift-item";
            div.innerHTML = `
                <a href="${nft.link}" target="_blank">
                    <img src="${nft.link}" alt="NFT Gift">
                </a>
                <p>${nft.name} - ${nft.series}</p>
                <p>${nft.price} TON</p>
            `;
            gallery.appendChild(div);
        });
    } catch (error) {
        console.error("Gagal mengambil data NFT:", error);
    }
}

// Muat NFT setiap 5 detik
setInterval(loadNFTs, 5000);
loadNFTs();