class FormHandler {
    constructor() {
        this.$form = $('.my-ajax-form');
        this.url = this.$form.data('url') || window.location.href;
        this.bindEvents();
    }

    bindEvents() {
        this.$form.on('submit', (event) => {
            event.preventDefault();
            this.submitForm();
        });
    }

    submitForm() {
        $.ajax({
            method: 'POST',
            url: this.url,
            data: this.$form.serialize(),
            success: this.handleFormSuccess.bind(this),
            error: this.handleFormError.bind(this),
        });
    }

    handleFormSuccess(response) {
        console.log(response);
        this.$form[0].reset();
        window.location.href = '../donation/confirm/';
    }

    handleFormError(jqXHR, textStatus, errorThrown) {
        console.error(textStatus, errorThrown);
    }
}

$(document).ready(() => {
    new FormHandler();
});