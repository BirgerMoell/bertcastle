import uuidv4 from 'uuid/v4'

async function _getJson (url) {
  const response = await fetch(url, {
    credentials: 'include',
    mode: 'cors'
  })
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}
Failed to GET ${url}`)
  }
  return response.json()
}

export const getJson = async function (url) {
  try {
    return await _getJson(url)
  } catch (err) {
    alert(err)
  }
}

export const postJson = async function (url, body) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText}
Failed to POST ${url}`)
    }
    return response.json()
  } catch (err) {
    alert(err)
  }
}

export const generateId = uuidv4

export const capitalize = s => s.replace(/^\w/, c => c.toUpperCase())
