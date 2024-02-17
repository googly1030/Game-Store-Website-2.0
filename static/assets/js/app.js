var isDragging = false;
var startX;
var scrollLeft;

document.addEventListener("mousedown", function (e) {
  var target = e.target.closest(".scroll, .scrollrow");

  if (!target) return;

  isDragging = true;
  startX = e.pageX - target.offsetLeft;
  scrollLeft = target.scrollLeft;
});

document.addEventListener("mouseup", function () {
  isDragging = false;
});

document.addEventListener("mousemove", function (e) {
  if (!isDragging) return;

  var target = e.target.closest(".scroll, .scrollrow");

  if (!target) return;

  var x = e.pageX - target.offsetLeft;
  var walk = (x - startX) * 2;
  target.scrollLeft = scrollLeft - walk;
});
document.addEventListener("DOMContentLoaded", function () {
  function toggleCardDetails() {
    var cardContent = document.querySelector(".card-content");
    var creditCardRadio = document.getElementById("creditCard");
    var paypalRadio = document.getElementById("paypal");
    var paypalContent = document.querySelector(".paypal-content");

    creditCardRadio.addEventListener("change", function () {
      if (creditCardRadio.checked) {
        cardContent.style.display = "block";
        paypalContent.style.display = "none";
        paypalRadio.checked = false;
      }
    });

    paypalRadio.addEventListener("change", function () {
      if (paypalRadio.checked) {
        cardContent.style.display = "none";
        paypalContent.style.display = "block";
        creditCardRadio.checked = false;
      }
    });
  }
  toggleCardDetails();
});

function placeOrder() {
  var placeOrderBtn = document.getElementById("placeOrderBtn");
  var orderStatus = document.getElementById("orderStatus");

  var spinner = placeOrderBtn.querySelector(".spinner-border");
  spinner.classList.remove("d-none");

  placeOrderBtn.disabled = true;

  setTimeout(function () {
    spinner.classList.add("d-none");

    placeOrderBtn.disabled = false;

    orderStatus.innerHTML =
      '<div class="alert alert-success" role="alert">Order Placed!</div>';
  }, 2000);
}

function addToWishlist(src, title, price, username) {
  console.log(username);
  if (username == "None") {
    alert("Please log in to add items to your cart.");
  } else {
    $.ajax({
      type: "POST",
      url: "/wishlist",
      data: {
        src: src,
        title: title,
        price: price,
      },
      success: function (response) {
        alert("Item added to wishlist successfully.");
      },
      error: function (xhr, status, error) {
        console.error(error);
      },
    });
  }
}

function addToCart(src, title, price, username) {
  console.log(username);
  if (username == "None") {
    alert("Please log in to add items to your cart.");
  } else {
    $.ajax({
      type: "POST",
      url: "/cart",
      data: {
        src: src,
        title: title,
        price: price,
      },
      success: function (response) {
        alert("Item added to cart successfully.");
      },
      error: function (xhr, status, error) {
        console.error(error);
      },
    });
  }
}

function wishListBtn() {
  $.ajax({
    url: "/wishlist",
    type: "GET",
    success: function (data) {
      console.log(data);
      $("body").html(data);
    },
    error: function (xhr, status, error) {
      console.error(error);
    },
  });
}

function cartListBtn() {
  $.ajax({
    url: "/cart",
    type: "GET",
    success: function (data) {
      console.log(data);
      $("body").html(data);
    },
    error: function (xhr, status, error) {
      console.error(error);
    },
  });
}

function remove_from_wishlist(item_id) {
  $.ajax({
    url: "/remove_from_wishlist",
    type: "POST",
    data: { item_id: item_id },
    success: function (response) {
      location.reload();
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
}

function remove_from_cart(item_id) {
  $.ajax({
    url: "/remove_from_cart",
    type: "POST",
    data: { item_id: item_id },
    success: function (response) {
      console.log(item_id);
      location.reload();
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
}

function filterGames(input) {
  var searchResultsContainer = document.getElementById("search-results");
  var searchResultsOverlay = document.getElementById("search-results-overlay");

  searchResultsContainer.innerHTML = "";

  var gameTitles = document.querySelectorAll(".card-title");
  var matchCount = 0;

  gameTitles.forEach(function (title) {
    if (title.innerText.toLowerCase().includes(input.toLowerCase())) {
      var resultItem = document.createElement("div");
      resultItem.innerText = title.innerText;
      searchResultsContainer.appendChild(resultItem);
      matchCount++;
    }
  });

  if (matchCount > 0) {
    searchResultsContainer.classList.add("show");
    searchResultsOverlay.classList.add("show");
  } else {
    searchResultsContainer.classList.remove("show");
    searchResultsOverlay.classList.remove("show");
  }
}

const Page1Data = [
  {
    imgUrl:
      "/static/assets/game imgs/genshin-impact-4-1920x1080-30df09f89d45.jpg",
    title: "Get started in Genshin Impact with our beginner’s guide",
    text: "These tips can help lighten the load for your trip through Teyvat",
  },
  {
    imgUrl:
      "/static/assets/game imgs/rainworldheader-3849x2165-458fc618b64d.jpg",
    title:
      "The secret mode that turns unforgiving platformer Rain World into a zen safari",
    text: "All the world’s a zoo in this postapocalyptic safari park",
  },
  {
    imgUrl: "/static/assets/game imgs/header-4k-3840x2160-f35c80a21a50.jpg",
    title:
      "For Valentine’s Day, we talk to Bugsnax’s developers about janky kisses and love",
    text: "Young Horses’ second outing tasks players with exa…earning something about themselves.",
  },
  {
    imgUrl: "/static/assets/game imgs/pubg.jpg",
    title: "What game genre is best for you?",
    text: "He likes League of Legends, I like Genshin Impact. What about you?",
  },
  {
    imgUrl: "/static/assets/game imgs/snowrunner.jpg",
    title: "SnowRunner is a trucking game where your only enemy is earth",
    text: "Under the hood of SnowRunner and the upcoming Expeditions: A Mudrunner Game",
  },
  {
    imgUrl: "/static/assets/game imgs/dyinglight 2.jpg",
    title:
      "Dying Light 2 celebrates a second birthday, eyes three more years of support",
    text: "Strong community support and a growing player base…e’ to continue improving the survival-horror epic",
  },
];
