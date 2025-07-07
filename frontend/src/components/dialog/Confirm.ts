import Swal, { SweetAlertIcon } from 'sweetalert2'

interface ConfirmOptions {
  title?: string
  text?: string
  icon?: SweetAlertIcon
  confirmButtonText?: string
  cancelButtonText?: string
}

export const confirmAction = async ({
  title = 'Are you sure?',
  text = 'This action cannot be undone.',
  icon = 'warning',
  confirmButtonText = 'Yes, proceed!',
  cancelButtonText = 'Cancel',
}: ConfirmOptions = {}) => {
  return await Swal.fire({
    title,
    text,
    icon,
    showCancelButton: true,
    confirmButtonText,
    cancelButtonText,
    customClass: {
      popup: 'swal-on-top',
    },
    reverseButtons: true,
    focusCancel: true,
  })
}