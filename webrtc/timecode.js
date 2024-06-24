  

function add_timecode(frame){return frame;}
function decode_timecode(frame){return;}

onmessage = ({data}) => {
        onrtctransform({transformer: data.rtctransform}); /* needed by chrome shim: */
  };

  onrtctransform = async ({transformer: {readable, writable, options}}) => {
    await readable.pipeThrough(new TransformStream({transform})).pipeTo(writable);

    function transform(chunk, controller) {

        const frame = "";
      /*
      if (options.side == "send"):
         frame = add_timecode(frame);
      else
         frame = decode_timecode(frame);
         */
     const metadata = chunk.getMetadata();
        console.log(options.side, metadata.frameId, metadata.synchronizationSource, chunk.timestamp)


      // console.log("FRAME!");
      var bytes = new Uint8Array(chunk.data);
      var offset = 100;
      bytes[offset]  =100;
      console.log(bytes[offset]);
      // bytes[offset] = 0xff;
      // bytes[offset+1] = 0xff;
      // bytes[offset+2] = 0xff;
      // bytes[offset+3] = 0xff;

      // const ts = new Uint8Array([8,8,8,8]);
      // const offset = 4; /* leave the first 4 bytes alone in VP8 */
      // for (let i = offset; i < bytes.length; i++) {
      //   bytes[i] = ~bytes[i]; /* XOR the rest */
      // }
      // if (options.side == "receive" && !descramble) {
      //   for (let i = offset+10; i < offset+12; i++) {
      //     bytes[i] = ~bytes[i]; /* reverse a few XOR for spectacle */
      //   }
      // }
      controller.enqueue(chunk);
    }
  };
