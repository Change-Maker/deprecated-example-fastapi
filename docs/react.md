# React

## Troubleshooting

- **Proxy to backend raised
  `options.allowedHosts[0] should be a non-empty string`**

  Refer to [create-react-app GitHub Issue #12304](https://github.com/facebook/create-react-app/issues/12304)

  **Re-produce:**
  1. Add `proxy` to `src/react_client/package.json`:

      ```jsonc
      {
        // ...
        "proxy": "http://localhost:3001"
      }
      ```

  2. Run the following command in `src/react_client/` folder to start react app:

      ```bash
      npm start
      ```

  3. The error raised:

      ```text
      Invalid options object. Dev Server has been initialized using an options object that does not match the API schema.
        - options.allowedHosts[0] should be a non-empty string.
      ```

  **Workaround:** Start react app with `DANGEROUSLY_DISABLE_HOST_CHECK`
  environment variable to be set to `true`:

  ```bash
  DANGEROUSLY_DISABLE_HOST_CHECK=true npm start
  ```
