package org.stos.carcassonne.tile.reader;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.ClassPathResource;

import java.io.IOException;
import java.io.InputStream;


public class TileLoader {

    private final ObjectMapper objectMapper = new ObjectMapper();

    public TileLoader() {
        objectMapper.findAndRegisterModules();
    }

    public TileDefinition load() {
        ClassPathResource resource = new ClassPathResource("test_data/test_tile.json");
        try (InputStream inputStream = resource.getInputStream()) {
            return objectMapper.readValue(inputStream, TileDefinition.class);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}