// Light DOM keeps Django's form, Tailwind styles, and HTMX visible to each other.
class ToggleForm extends HTMLElement {
    constructor() {
        super();
        this.isOpen = false;
        this.animation = null;
        this.handleClick = () => this.toggle();
    }

    connectedCallback() {
        // The deferred script and HTMX fragments supply the child HTML first.
        this.button = this.querySelector("[data-toggle]");
        this.form = this.querySelector("[data-toggle-content]");
        if (!this.button || !this.form) return;

        this.isOpen = !this.form.hidden;
        this.render();
        this.button.addEventListener("click", this.handleClick);
    }

    disconnectedCallback() {
        // HTMX removes old instances when it replaces the quote panel.
        this.button?.removeEventListener("click", this.handleClick);
        this.animation?.cancel();
        this.animation = null;
        if (this.form) {
            this.form.style.overflow = "";
            this.form.hidden = !this.isOpen;
        }
    }

    toggle() {
        this.isOpen = !this.isOpen;
        this.render(true);
    }

    render(animate = false) {
        this.button.textContent = this.isOpen ? "Hide form" : "New quote";
        this.button.setAttribute("aria-expanded", String(this.isOpen));
        // Measure the current frame before cancelling, so rapid clicks reverse smoothly.
        const startHeight = this.form.hidden ? 0 : this.form.getBoundingClientRect().height;
        const startOpacity = this.form.hidden ? 0 : Number(getComputedStyle(this.form).opacity);
        this.animation?.cancel();
        this.animation = null;
        this.form.style.overflow = "";
        this.form.inert = !this.isOpen;

        if (!animate || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            this.form.hidden = !this.isOpen;
            if (animate) this.focusControl();
            return;
        }

        // Keep the content rendered until the closing animation finishes.
        this.form.hidden = false;
        const endHeight = this.isOpen ? this.form.getBoundingClientRect().height : 0;
        this.form.style.overflow = "hidden";
        if (!this.isOpen) this.button.focus();

        const animation = this.form.animate([
            { height: `${startHeight}px`, opacity: startOpacity },
            { height: `${endHeight}px`, opacity: this.isOpen ? 1 : 0 },
        ], { duration: 220, easing: "ease-in-out" });
        this.animation = animation;

        animation.onfinish = () => {
            if (this.animation !== animation) return;
            this.animation = null;
            this.form.hidden = !this.isOpen;
            this.form.style.overflow = "";
            // Natural height after completion accommodates errors and resizing.
            if (this.isOpen && document.activeElement === this.button) this.focusControl();
        };
    }

    focusControl() {
        if (this.isOpen) {
            this.form.querySelector(
                "[aria-invalid='true'], input:not([type='hidden']), select"
            )?.focus();
        } else {
            this.button.focus();
        }
    }
}

// The browser initializes every <toggle-form>, including future HTMX inserts.
customElements.define("toggle-form", ToggleForm);

// Initialization is automatic; this listener only restores keyboard focus.
document.addEventListener("htmx:afterSwap", (event) => {
    if (event.target instanceof Element && event.target.id === "quote-panel") {
        const component = event.target.querySelector("toggle-form");
        if (component instanceof ToggleForm) component.focusControl();
    }
});
