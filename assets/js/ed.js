// 'Back to top' logic
function setupBackToTop() {
  const intersectionObserver = new IntersectionObserver(function(entries) {
    const topBtn = document.querySelector('.top-of-site-link');
    if (topBtn === null) return;

    topBtn.dataset.visible = entries[0].boundingClientRect.y < 0;
  });

  const topAnchor = document.querySelector('#top-of-site-anchor');
  if (topAnchor !== null) {
    intersectionObserver.observe(topAnchor);
  }
}

// Annotation support
function setupHypothes() {
  const hypothesisContainer = document.querySelector('.hypothesis-container');
  if (hypothesisContainer !== null) {
    hypothesisContainer.addEventListener('click', e => {
      e.preventDefault();

      let script = document.createElement('script');
      script.setAttribute('src', 'https://cdn.hypothes.is/hypothesis');
      script.type = 'text/javascript';
      document.getElementsByTagName('head')[0].appendChild(script);
    });
  }

  const hypothesisLink = document.querySelector('#hypothesis-link');
  if (hypothesisLink !== null) {
    hypothesisContainer.addEventListener('click', e => e.preventDefault());
  }
}

function setupSideBarAutoClose() {
  const sidebarLinks = document.querySelectorAll(".sidebar-nav-item");
  const sidebarToggle = document.querySelector(".sidebar-toggle");

  sidebarLinks.forEach(link => {
    link.addEventListener("click", () => {
      if (sidebarToggle)
        sidebarToggle.click();
    });
  });
}

function setupImageLightBox() {
  const postImages = document.querySelectorAll(".post-body img");
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-img");

  if (!lightbox || !lightboxImg)
    return;

  postImages.forEach(img => {
    img.addEventListener("click", () => {
      lightboxImg.src = img.src;
      lightboxImg.alt = img.alt;
      lightbox.classList.add("open");
    });
  });
}

function fixBottomVoid() {
  console.log("Fixing Bottom Void");
  const bottomElement = document.getElementById("bottom-element");
  const voidMark = document.getElementById("void-mark");
  const heavenMark = document.getElementById("heaven-mark");

  console.log("Found Bottom Element" + bottomElement + ", " + voidMark);
  const rect = bottomElement.getBoundingClientRect();
  const vpHeight = window.innerHeight;

  if (rect.bottom < vpHeight) {
    const gap = vpHeight - rect.bottom;

    const voidSpacer = document.createElement("div");
    voidSpacer.id = "void-spacer";
    voidSpacer.style.height = Math.floor(gap / 2) + "px";
    voidSpacer.style.pointerEvents = "none";

    const heavenSpacer = document.createElement("div");
    heavenSpacer.id = "heaven-spacer";
    heavenSpacer.style.height = Math.ceil(gap / 2) + "px"
    heavenSpacer.style.pointerEvents = "none";

    console.log("Inserting spaces of " + gap / 2 + "px");
    voidMark.parentNode.insertBefore(voidSpacer, voidMark);
    heavenMark.parentNode.insertBefore(heavenSpacer, heavenMark);
  }
}

function debounce(func, delay) {
  let timerId;
  return function(...args) {
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      func.apply(this, args)
    }, delay);
  }
}

const fixBottomVoidDebounced = debounce(fixBottomVoid, 1000);

document.addEventListener('DOMContentLoaded', () => {
  setupBackToTop();
  setupHypothes();
  setupSideBarAutoClose();
  setupImageLightBox();
  fixBottomVoid();
  
  window.addEventListener("resize", () => {
    fixBottomVoidDebounced();
  });
});
