import Swal from 'sweetalert2'

export const confirmUpdate = async () => {
  return await Swal.fire({
    title: 'Confirm Update',
    text: 'Are you sure you want to update this IP?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, update it!',
    cancelButtonText: 'Cancel',
    customClass: {
      popup: 'swal-on-top'
    }
  })
}
