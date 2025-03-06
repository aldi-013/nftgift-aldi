document.addEventListener("DOMContentLoaded", function() {
  fetch("data.json")
    .then(response => response.json())
    .then(data => {
      let gallery = document.getElementById("gallery");
      data.forEach(item => {
        let div = document.createElement("div");
        div.className = "gift-item";
        div.innerHTML = `<a href="${item.link}" target="_blank">
                                    <img src="${item.link}" alt="NFT Gift">
                                 </a>`;
        gallery.appendChild(div);
      });
    });
});

function searchGift() {
  let input = document.getElementById("search").value.toLowerCase();
  let gifts = document.querySelectorAll(".gift-item");

  gifts.forEach(gift => {
    let link = gift.querySelector("a").href.toLowerCase();
    if (link.includes(input)) {
      gift.style.display = "block";
    } else {
      gift.style.display = "none";
    }
  });
}
