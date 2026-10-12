document.addEventListener("DOMContentLoaded", () => {

    const choices = document.querySelector(".choices");

    choices.addEventListener("click", (event) => {
        if (event.target.id ==  "ingredientButton") {
            ingredientChoice.style.display = "block";
            mealChoice.style.display = "none"
        } else {
            mealChoice.style.display = "flex";
            ingredientChoice.style.display = "none";
        }
    });

    const resultsList = document.getElementById("resultsList");
    const detailsBox = document.querySelector(".detailsBox");

    if (!resultsList || !detailsBox) return;

    const GAP = 10;
    let activeTile = null;

    resultsList.addEventListener("click", (event) => {
        const tile = event.target.closest(".mealTile");
        if (!tile) return;

        if (tile === activeTile) {
            detailsBox.classList.remove("visible");
            activeTile = null;
            return;
        }
        activeTile = tile;

        detailsBox.classList.add("visible");

        const containerWidth = resultsList.clientWidth;
        const containerHeight = resultsList.clientHeight;
        const boxWidth = detailsBox.offsetWidth;
        const boxHeight = detailsBox.offsetHeight;

        const tileLeft = tile.offsetLeft;
        const tileTop = tile.offsetTop - resultsList.scrollTop;
        const tileRight = tileLeft + tile.offsetWidth;
        const tileCenterY = tileTop + tile.offsetHeight / 2;

        // Put the box on whichever side of the tile has more room, so it stays attached to it.
        const roomOnRight = containerWidth - tileRight;
        const roomOnLeft = tileLeft;
        const goRight = roomOnRight >= roomOnLeft;

        let left = goRight ? tileRight + GAP : tileLeft - GAP - boxWidth;
        left = Math.max(GAP, Math.min(left, containerWidth - boxWidth - GAP));

        let top = tileCenterY - boxHeight / 2;
        top = Math.max(GAP, Math.min(top, containerHeight - boxHeight - GAP));

        detailsBox.style.left = `${left}px`;
        detailsBox.style.top = `${top}px`;
        detailsBox.style.right = "auto";
        detailsBox.style.bottom = "auto";
    });

    
});


    




