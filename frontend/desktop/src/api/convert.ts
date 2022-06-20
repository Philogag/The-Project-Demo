
function convert (data, fn_key_rebuild) {
  if (typeof data !== 'object' || !data) return data
  if (Array.isArray(data)) {
    return data.map(item => convert(item, fn_key_rebuild))
  }

  let newObj = {}
  for (const key in data) {
    if (Object.prototype.hasOwnProperty.call(data, key)) {
      let newKey = fn_key_rebuild(key)
      newObj[newKey] = convert(data[key], fn_key_rebuild)
    }
  }
  return newObj
}

export function convertUnderlineToCamel(data) {
  return convert(data, (key) => key.replace(/_([a-z0-9])/g, res => res[1].toUpperCase()))
}

export function convertCamelToUnderline(data) {
  //@ts-ignore
  return convert(data, (key) => key.replace(/([A-Z]|\d+)/g, (p, m) => `_${m.toLowerCase()}`))
}
