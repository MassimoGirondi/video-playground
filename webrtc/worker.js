// Code from https://github.com/w3c/webrtc-encoded-transform/blob/main/explainer.md

  // Sender transform
  function createSenderTransform() {
    return new TransformStream({
      start() {
        // Called on startup.
      },

      async transform(frame, controller) {
        // let view = new DataView(encodedFrame.data);
        // // Create a new buffer with 4 additional bytes.
        // let newData = new ArrayBuffer(encodedFrame.data.byteLength + 4);
        // let newView = new DataView(newData);


        const canvas = new OffscreenCanvas(1, 1);
        const ctx = canvas.getContext('2d');
        const intTxtFontSize = 100;
        let x = 100;
        const position="bottom";

        const width = frame.displayWidth;
        const height = frame.displayHeight;
        canvas.width = width;
        canvas.height = height;

        const bgHeight = intTxtFontSize + bgPadding;
        const bgPositionY = position === 'bottom'
          ? height - (intTxtFontSize + bgPadding + 5)
          : 5;
        const txtPositionY = position === 'bottom'
          ? height - (Math.floor(bgPadding / 2) + 10)
          : 5 + intTxtFontSize;

        ctx.clearRect(0, 0, width, height);
        ctx.drawImage(frame, 0, 0, width, height);
        ctx.font = txtFontSize + ' ' + 'sans-serif";
        ctx.fillStyle = 'black';
        ctx.fillRect(0, bgPositionY, width, bgHeight)
        ctx.fillStyle = txtColor;
        ctx.fillText(text, 0, txtPositionY);
        const newFrame = new VideoFrame(canvas, { timestamp: frame.timestamp });
        frame.close();

        // Send it to the output stream.
        //controller.enqueue(encodedFrame);
        controller.enqueue(newFrame);
      },

      flush() {
        // Called when the stream is about to be closed.
      }
    });
  }


  function createReceiverTransform() {
    return new TransformStream({
      start() {},
      flush() {},
      async transform(encodedFrame, controller) {
        // // Reconstruct the original frame.
        const view = new DataView(encodedFrame.data);

        // // Ignore the last 4 bytes
        const newData = new ArrayBuffer(encodedFrame.data.byteLength - 4);
        const newView = new DataView(newData);

        // // Negate all bits in the incoming frame, ignoring the
        // // last 4 bytes
        // for (let i = 0; i < encodedFrame.data.byteLength - 4; ++i)
        //   newView.setInt8(i, ~view.getInt8(i));

        // encodedFrame.data = newData;
        controller.enqueue(encodedFrame);
      }
    });
  }

onrtctransform = (event) => {
  let transform;
  if (event.transformer.options.name == "senderTransform")
    transform = createSenderTransform(); // returns a TransformStream
  else if (event.transformer.options.name == "receiverTransform")
    transform = createReceiverTransform(); // returns a TransformStream
  else return;
  event.transformer.readable
    .pipeThrough(transform)
    .pipeTo(event.transformer.writable);
};
