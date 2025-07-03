export const validateIPFormat = (ip: string) => {
  const ipv4 = /^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$/;
  const ipv6 = /^(([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4}|:)|(([0-9a-fA-F]{1,4}:){1,7}:)|(::([0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}))$/;
  return ipv4.test(ip) || ipv6.test(ip);
};

export const validateIPForm = ({
  ip,
  label,
  isEdit
}: {
  ip: string;
  label: string;
  isEdit?: boolean;
}) => {
  const errors: { ip?: string; label?: string } = {};
  if (!label.trim()) {
    errors.label = 'Label is required';
  }
  if (!isEdit) {
    if (!ip.trim()) {
      errors.ip = 'IP address is required';
    } else if (!validateIPFormat(ip.trim())) {
      errors.ip = 'Invalid IP address';
    }
  }
  return errors;
};
