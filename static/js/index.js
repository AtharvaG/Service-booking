var light = $("#red-light"),
                cap = $("#cap"),
                lens = $("#camera-lens"),
                tape = $("#camera-tape"),
                text = $(".text-enter"),
                textStatement = $(".text-animation p"),
                tl = new TimelineMax(),
                textTl = new TimelineMax();

            tl.to(cap, 0.3, { autoAlpha: 1, delay: 0.3 })
                .fromTo(tape, 0.4, {yPercent: 100, autoAlpha: 0}, { yPercent: 0, autoAlpha: 1, delay: 0.3, ease: Bounce.easeOut }, 0.6)
                .fromTo(lens, 0.4, {scale: 0.5, autoAlpha: 0, transformOrigin: 'center center'}, { scale: 1, autoAlpha: 1, delay: 0.3, ease: Bounce.easeOut }, 0.6)
                .to(light, 0.75, { fill: "#c43235", repeat: -1, yoyo: true });

textTl.staggerFromTo(text, 0.75, {yPercent: 100, autoAlpha: 0}, {yPercent: 0, autoAlpha: 1, ease: Bounce.easeOut}, 0.2)
.to(text, 0.5, {yPercent: 100, delay: 0.3, autoAlpha: 0})
.fromTo(textStatement, 0.75, {yPercent: 100, autoAlpha: 0}, {yPercent: 1, delay: 0.5, autoAlpha: 1, ease: Expo.easeOut});