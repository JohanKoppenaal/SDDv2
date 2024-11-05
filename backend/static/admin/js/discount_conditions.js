document.addEventListener('DOMContentLoaded', function() {
    function updateShopwareValues(row) {
        if (!row) return;

        const typeSelect = row.querySelector('select[name*="-condition_type"]');
        const valueSelect = row.querySelector('select[name*="-shopware_value"]');

        if (!typeSelect || !valueSelect) return;

        typeSelect.addEventListener('change', function() {
            // Reset value select
            valueSelect.innerHTML = '<option value="">-----</option>';
            valueSelect.disabled = true;

            const type = this.value;
            if (!type) return;

            // Haal nieuwe waardes op
            fetch(`/admin/discounts/get-shopware-values/${type}/`)
                .then(response => response.json())
                .then(data => {
                    valueSelect.disabled = false;
                    if (Array.isArray(data)) {
                        data.forEach(item => {
                            const option = new Option(item.name, item.id);
                            valueSelect.add(option);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    valueSelect.disabled = false;
                });
        });
    }

    // Update bestaande rijen
    document.querySelectorAll('.inline-related').forEach(row => {
        if (row instanceof HTMLElement) {
            updateShopwareValues(row);
        }
    });

    // Voor Django admin inline formsets
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery(document).on('formset:added', function(event, $row) {
            if ($row && $row[0]) {
                updateShopwareValues($row[0]);
            }
        });
    }
});
