# Super Find-a-Part: inventory search AI agent

Obtain and build [llama.cpp](https://llama-cpp.com/):

    git clone https://github.com/ggerganov/llama.cpp
    cd llama.cpp
    cmake -B build -S . -DGGML_CUDA=ON
    cmake --build build -j

Obtain the [Gemma 3](https://huggingface.co/bartowski/google_gemma-3-12b-it-GGUF) model
and start the LLM server:

    llama-server -m ~/temp/gemma-3-12b-it-UD-IQ3_XXS.gguf \
       --port 8080 -c 4096 -ngl 999

To build the inventory file: Put PDF datasheets into the `pdf/` directory and
call `make`.
