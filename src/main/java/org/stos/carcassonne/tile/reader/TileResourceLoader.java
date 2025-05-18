package org.stos.carcassonne.tile.reader;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import org.stos.carcassonne.tile.reader.type.TileDefinition;

import java.io.IOException;
import java.io.InputStream;

@Service
public class TileResourceLoader {

    private final ObjectMapper objectMapper;

    public TileResourceLoader(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
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