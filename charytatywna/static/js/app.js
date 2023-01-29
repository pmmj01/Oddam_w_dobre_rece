document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            // e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */

        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();

                    if (this.currentStep === 5) {
                        const quantity = document.querySelector('input[name="quantity"]').value
                        const quantity_summary = document.getElementById('quantity')
                        const categories = []
                        const category = document.querySelectorAll('input[type="checkbox"]:checked')
                        category.forEach(id => {
                            categories.push(' ' + id.getAttribute('data-id'))
                        })
                        if (parseInt(quantity) === 1) {
                            quantity_summary.innerText = quantity + ' worek z: ' + categories;
                        } else if (parseInt(bags) < 5) {
                            quantity_summary.innerText = quantity + ' worki z: ' + categories;
                        } else {
                            quantity_summary.innerText = quantity + ' worków z: ' + categories;
                        }
                        const institution_checked = document.querySelector('input[type="radio"]:checked');
                        const institution = institution_checked.getAttribute('data-id')
                        const institution_summary = document.getElementById('institution')
                        institution_summary.innerText = 'Dla ' + institution

                        const address = document.querySelector('input[name="address"]').value
                        const address_summary = document.getElementById('address')
                        address_summary.innerText = address

                        const city = document.querySelector('input[name="city"]').value
                        const city_summary = document.getElementById('city')
                        city_summary.innerText = city

                        const zip_code = document.querySelector('input[name="zip_code"]').value
                        const zip_code_summary = document.getElementById('zip_code')
                        zip_code_summary.innerText = zip_code

                        const phone_number = document.querySelector('input[name="phone_number"]').value
                        const phone_number_summary = document.getElementById('phone_number')
                        phone_number_summary.innerText = phone_number

                        const pick_up_date = document.querySelector('input[name="pick_up_date"]').value
                        const pick_up_date_summary = document.getElementById('pick_up_date')
                        pick_up_date_summary.innerText = pick_up_date

                        const pick_up_time = document.querySelector('input[name="pick_up_time"]').value
                        const pick_up_time_summary = document.getElementById('pick_up_time')
                        pick_up_time_summary.innerText = pick_up_time

                        const pick_up_coment = document.querySelector('textarea[name="pick_up_comment"]').value
                        const pick_up_coment_summary = document.getElementById('pick_up_comment')
                        if (pick_up_coment !== "") {
                            pick_up_coment_summary.innerText = pick_up_coment
                        } else {
                            pick_up_coment_summary.innerText = "Brak uwag"
                        }

                    }
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            let multiForm = this.$form.querySelector("form")
            let summary = document.querySelectorAll(".summary--text")
            let address = document.querySelector(".summary--address")
            let delivery = document.querySelector(".summary--delivery")
            let quantity = multiForm.elements['quantity'].value.toString()
            let categories = multiForm.querySelectorAll('input[name="categories"]:checked')
            let institution = multiForm.querySelector('input[name="institution"]:checked').dataset
            let street = multiForm.querySelector('input[name="address"]').value
            let city = multiForm.querySelector('input[name="city"]').value
            let zip_code = multiForm.querySelector('input[name="zip_code"]').value
            let phone_number = multiForm.querySelector('input[name="phone_number"]').value
            let pick_up_date = multiForm.querySelector('input[name="pick_up_date"]').value
            let pick_up_time = multiForm.querySelector('input[name="pick_up_time"]').value
            let pick_up_comment = document.querySelector('#pick_up_comment').value


            if (bags === '1') {
                summary[0].innerText = bags + ' worek'
            } else if (bags.slice(-1) === '2' || bags.slice(-1) === '3' || bags.slice(-1) === '4') {
                summary[0].innerText = bags + ' worki'
            } else {
                summary[0].innerText = bags + ' worków'
            }
            summary[1].innerText = institution.type + ' ' + institution.name
            address.children[0].innerText = street
            address.children[1].innerText = city
            address.children[2].innerText = zip_code
            address.children[3].innerText = phone_number
            delivery.children[0].innerText = pick_up_date
            delivery.children[1].innerText = pick_up_time
            delivery.children[2].innerText = pick_up_comment

        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            // e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    // Pobierz formularz
    const forms = document.querySelector('#donation-form');

    // Nasłuchuj submit formularza
    forms.addEventListener('submit', (e) => {
        e.preventDefault();

        // Pobierz wartości z formularza
        const category = forms.elements.category.value;
        const quantity = forms.elements.quantity.value;
        const institution = forms.elements.institution.value;
        const address = forms.elements.address.value;
        const city = forms.elements.city.value;
        const zip_code = forms.elements.zip_code.value;
        const phone_number = forms.elements.phone_number.value;
        const pick_up_date = forms.elements.pick_up_date.value;
        const pick_up_time = forms.elements.pick_up_time.value;
        const pick_up_comment = forms.elements.pick_up_comment.value;
    });


    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }


    function editUser(pk) {
        let form = document.getElementById('edit-user-form');
        let data = new FormData(form);
        fetch(`/user/${pk}/`, {
            method: 'POST',
            body: data,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then((response) => {
                if (response.ok) {
                    alert('Użytkownik został zaktualizowany');
                    location.reload();
                } else {
                    alert('Wystąpił błąd podczas edytowania użytkownika');
                }
            })
            .catch((error) => {
                console.log(error);
                alert('Wystąpił błąd podczas edytowania użytkownika');
            });
    }


    function deleteUser(pk) {
        if (confirm("Czy na pewno chcesz usunąć tego użytkownika?")) {
            fetch(`/user/${pk}/delete/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
                .then((response) => {
                    if (response.ok) {
                        alert('Użytkownik został usunięty');
                        location.reload();
                    } else {
                        alert('Wystąpił błąd podczas usuwania użytkownika');
                    }
                })
                .catch((error) => {
                    console.log(error);
                    alert('Wystąpił błąd podczas usuwania użytkownika');
                });
        }
    }


});
